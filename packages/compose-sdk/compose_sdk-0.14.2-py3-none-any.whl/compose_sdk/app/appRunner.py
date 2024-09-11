import inspect
from typing import Any, TypedDict, Callable, Union

from ..scheduler import Scheduler
from ..api import (
    ApiHandler,
    encode_string,
    encode_num_to_four_bytes,
    combine_buffers,
)
from ..core import (
    Utils,
    EventType,
    Render,
    ComponentInstance,
    INTERACTION_TYPE,
    TYPE,
    JSON,
    page_confirm,
    CONFIRM_APPEARANCE,
    CONFIRM_APPEARANCE_DEFAULT,
)

from .appDefinition import AppDefinition
from .state import State
from .page import Page, Config as PageConfig, Params as PageParams


class ConfirmationDialog(TypedDict):
    id: str
    is_active: bool
    resolve: Callable[[bool], None]


class AppRunner:
    def __init__(
        self,
        scheduler: Scheduler,
        api: ApiHandler,
        appDefinition: AppDefinition,
        executionId: str,
        browserSessionId: str,
    ):
        self.scheduler = scheduler
        self.api = api
        self.appDefinition = appDefinition
        self.executionId = executionId
        self.browserSessionId = browserSessionId

        self.renders = {}
        self.tempFiles = {}

        self.confirmationDialog: Union[ConfirmationDialog, None] = None

    async def render_ui(self, layout: Any) -> Any:
        try:
            future = self.scheduler.create_future()

            def resolve_render(data=None):
                if not future.done():
                    future.set_result(data)

            renderId = Utils.generate_id()

            static_layout = Render.generate_static_layout(layout, resolve_render)

            self.renders[renderId] = {
                "resolve": resolve_render,
                "is_resolved": False,
                "layout": layout,
                "static_layout": static_layout,
                "comparison_layout": static_layout,
            }

            await self.api.send(
                {
                    "type": EventType.SdkToServer.RENDER_UI,
                    "ui": static_layout,
                    "executionId": self.executionId,
                    "renderId": renderId,
                },
                self.browserSessionId,
            )
        except Exception as error:
            await self.__send_error(
                f"An error occurred in the page.add fragment:\n\n{str(error)}"
            )

        return await future

    async def confirm(
        self,
        *,
        title: str = None,
        message: str = None,
        type_to_confirm_text: str = None,
        confirm_button_label: str = None,
        cancel_button_label: str = None,
        appearance: CONFIRM_APPEARANCE = CONFIRM_APPEARANCE_DEFAULT,
    ):
        if self.confirmationDialog is not None and self.confirmationDialog["is_active"]:
            await self.__send_error(
                "Trying to open a confirmation dialog while another one is already open"
            )

            return False

        future = self.scheduler.create_future()

        def resolve_confirm(response: bool):
            if not future.done():
                self.confirmationDialog["is_active"] = False
                future.set_result(response)

        id = Utils.generate_id()

        self.confirmationDialog = {
            "id": id,
            "is_active": True,
            "resolve": resolve_confirm,
        }

        component = page_confirm(
            id,
            resolve_confirm,
            title=title,
            message=message,
            type_to_confirm_text=type_to_confirm_text,
            confirm_button_label=confirm_button_label,
            cancel_button_label=cancel_button_label,
            appearance=appearance,
        )

        await self.api.send(
            {
                "type": EventType.SdkToServer.CONFIRM,
                "executionId": self.executionId,
                "component": component,
            },
            self.browserSessionId,
        )

        return await future

    async def set_config(self, config: PageConfig):
        await self.api.send(
            {
                "type": EventType.SdkToServer.PAGE_CONFIG,
                "config": config,
                "executionId": self.executionId,
            },
            self.browserSessionId,
        )

    async def on_state_update(self):
        updated_renders = {}

        for renderId in self.renders:
            layout = self.renders[renderId]["layout"]

            # No need to check for changes for static layouts
            if not callable(layout):
                continue

            resolve_fn = self.renders[renderId]["resolve"]

            try:
                new_static_layout = Render.generate_static_layout(layout, resolve_fn)
            except Exception as error:
                return await self.__send_error(
                    f"An error occurred while re-rendering the UI:\n\n{str(error)}"
                )

            # new_comparison_layout = JSON.stringify(
            #     Render.static_layout_without_ids(new_static_layout)
            # )

            # Quick and dirty check to see if the layout has changed.
            # if new_comparison_layout == self.renders[renderId]["comparison_layout"]:
            #     continue

            updated_renders[renderId] = new_static_layout

            self.renders[renderId]["static_layout"] = new_static_layout
            # self.renders[renderId]["comparison_layout"] = new_comparison_layout

        if len(updated_renders) > 0:
            await self.api.send(
                {
                    "type": EventType.SdkToServer.RERENDER_UI,
                    "diff": updated_renders,
                    "executionId": self.executionId,
                },
                self.browserSessionId,
            )

    async def download(self, file: bytes, filename: str):
        metadata = {
            "name": filename,
            "download": True,
            "executionId": self.executionId,
            "id": Utils.generate_id(),
        }

        metadata_str = JSON.stringify(metadata)

        header_binary = encode_string(
            EventType.SdkToServer.FILE_TRANSFER + self.browserSessionId
        )

        metadata_length_binary = encode_num_to_four_bytes(len(metadata_str))

        metadata_binary = encode_string(metadata_str)

        message = combine_buffers(
            header_binary, metadata_length_binary, metadata_binary, file
        )

        await self.api.send_raw(message)

    async def link(
        self, appRouteOrUrl: str, newTab: bool = True, params: PageParams = {}
    ):
        await self.api.send(
            {
                "type": EventType.SdkToServer.LINK,
                "appRouteOrUrl": appRouteOrUrl,
                "newTab": newTab,
                "executionId": self.executionId,
                "params": params,
            },
            self.browserSessionId,
        )

    async def reload(self):
        await self.api.send(
            {
                "type": EventType.SdkToServer.RELOAD_PAGE,
                "executionId": self.executionId,
            },
            self.browserSessionId,
        )

    async def __send_error(self, errorMsg: str):
        await self.api.send(
            {
                "type": EventType.SdkToServer.APP_ERROR,
                "errorMessage": errorMsg,
                "executionId": self.executionId,
            },
            self.browserSessionId,
        )

    async def execute(self, params: PageParams):
        page = Page(self, params)
        state = State(self, self.appDefinition.initial_state)

        try:
            handler = self.appDefinition.handler
            handler_params = inspect.signature(handler).parameters
            kwargs = {}
            if "page" in handler_params:
                kwargs["page"] = page
            if "state" in handler_params:
                kwargs["state"] = state
            if "ui" in handler_params:
                kwargs["ui"] = ComponentInstance

            if inspect.iscoroutinefunction(self.appDefinition.handler):
                await self.appDefinition.handler(**kwargs)
            else:
                self.appDefinition.handler(**kwargs)
        except Exception as error:
            await self.__send_error(
                f"An error occurred while running the app:\n\n{str(error)}"
            )

    async def on_click_hook(self, component_id: str, render_id: str):
        if render_id not in self.renders:
            return

        static_layout = self.renders[render_id]["static_layout"]

        component = Render.find_component_by_id(static_layout, component_id)

        if (
            component is None
            or component["interactionType"] is not INTERACTION_TYPE.BUTTON
        ):
            return

        hookFunc = component["hooks"]["onClick"]

        if hookFunc is not None:
            await self.hook_error_handler(hookFunc)

    async def on_submit_form_hook(
        self, form_component_id: str, render_id: str, form_data: dict
    ):
        if render_id not in self.renders:
            return

        hydrated, temp_files_to_delete = Render.hydrate_form_data(
            form_data, self.tempFiles
        )

        for file_id in temp_files_to_delete:
            del self.tempFiles[file_id]

        static_layout = self.renders[render_id]["static_layout"]
        component = Render.find_component_by_id(static_layout, form_component_id)

        if component is None or component["type"] != TYPE.LAYOUT_FORM:
            return

        input_errors = Render.get_form_input_errors(hydrated, static_layout)
        form_error = Render.get_form_error(component, hydrated)

        if input_errors is not None or form_error is not None:
            await self.api.send(
                {
                    "type": EventType.SdkToServer.FORM_VALIDATION_ERROR,
                    "renderId": render_id,
                    "inputComponentErrors": input_errors,
                    "formError": form_error,
                    "executionId": self.executionId,
                    "formComponentId": form_component_id,
                },
                self.browserSessionId,
            )

            return

        hookFunc = component["hooks"]["onSubmit"]

        if hookFunc is not None:
            await self.api.send(
                {
                    "type": EventType.SdkToServer.FORM_SUBMISSION_SUCCESS,
                    "executionId": self.executionId,
                    "renderId": render_id,
                    "formComponentId": form_component_id,
                },
                self.browserSessionId,
            )
            await self.hook_error_handler(lambda: hookFunc(hydrated))

    async def on_input_hook(
        self, event_type: str, component_id: str, render_id: str, value: any
    ):
        if render_id not in self.renders:
            return

        hydrated, temp_files_to_delete = Render.hydrate_form_data(
            {component_id: value}, self.tempFiles
        )

        for file_id in temp_files_to_delete:
            del self.tempFiles[file_id]

        static_layout = self.renders[render_id]["static_layout"]
        component = Render.find_component_by_id(static_layout, component_id)

        if component is None or component["interactionType"] != INTERACTION_TYPE.INPUT:
            return

        input_errors = Render.get_form_input_errors(hydrated, static_layout)

        if input_errors is not None:
            error = input_errors[component_id]

            await self.api.send(
                {
                    "type": EventType.SdkToServer.INPUT_VALIDATION_ERROR,
                    "renderId": render_id,
                    "executionId": self.executionId,
                    "error": error,
                    "componentId": component_id,
                },
                self.browserSessionId,
            )

            return

        hookFunc = None
        if event_type == EventType.ServerToSdk.ON_ENTER_HOOK:
            hookFunc = component["hooks"]["onEnter"]
        elif event_type == EventType.ServerToSdk.ON_SELECT_HOOK:
            hookFunc = component["hooks"]["onSelect"]
        elif event_type == EventType.ServerToSdk.ON_FILE_CHANGE_HOOK:
            hookFunc = component["hooks"]["onFileChange"]

        if hookFunc is not None:
            await self.hook_error_handler(lambda: hookFunc(hydrated[component_id]))

    async def on_table_row_action_hook(
        self, component_id: str, render_id: str, action_idx: int, value: any
    ):
        if render_id not in self.renders:
            await self.__send_error(
                "An error occurred while trying to execute a table row action hook:\n\nThe render container was not found"
            )
            return

        static_layout = self.renders[render_id]["static_layout"]
        component = Render.find_component_by_id(static_layout, component_id)

        if component is None:
            await self.__send_error(
                "An error occurred while trying to execute a table row action hook:\n\nThe component was not found"
            )
            return

        if component["type"] != TYPE.INPUT_TABLE:
            await self.__send_error(
                "An error occurred while trying to execute a table row action hook:\n\nThe component is not a table"
            )
            return

        if (
            component["hooks"]["onRowActions"] is None
            or len(component["hooks"]["onRowActions"]) <= action_idx
        ):
            await self.__send_error(
                "An error occurred while trying to execute a table row action hook:\n\nThe row action was not found"
            )
            return

        hookFunc = component["hooks"]["onRowActions"][action_idx]
        await self.hook_error_handler(lambda: hookFunc(value))

    async def on_confirm_response_hook(self, id: str, response: bool):
        if self.confirmationDialog is None or self.confirmationDialog["id"] != id:
            await self.__send_error(
                "An error occurred while trying to resolve a confirmation dialog:\n\nThe confirmation dialog was not found"
            )
            return

        self.confirmationDialog["resolve"](response)

    def on_file_transfer(self, file_id: str, file_contents: bytes):
        self.tempFiles[file_id] = file_contents

    async def hook_error_handler(self, func):
        try:
            func()
        except Exception as error:
            await self.__send_error(
                f"An error occurred while executing a callback function:\n\n{str(error)}"
            )
