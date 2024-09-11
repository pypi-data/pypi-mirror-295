from typing import TYPE_CHECKING, Any, Awaitable, TypedDict, Union, Callable
from ..core import ComponentReturn, CONFIRM_APPEARANCE, CONFIRM_APPEARANCE_DEFAULT

if TYPE_CHECKING:
    from .appRunner import AppRunner


class Config(TypedDict, total=False):
    width: str


resolve = Callable[[Any], None]
staticLayout = Union[ComponentReturn, list[ComponentReturn]]

Params = dict[str, str | int | bool | None]


class Page:
    def __init__(self, appRunner: "AppRunner", params: Params):
        self.__appRunner = appRunner
        self.__params = params if params is not None else {}

    @property
    def params(self) -> Params:
        return self.__params

    def add(
        self,
        layout: Union[
            staticLayout, Callable[[resolve], staticLayout], Callable[[], staticLayout]
        ],
    ) -> Awaitable[Any] | Any:
        return self.__appRunner.scheduler.ensure_future(
            self.__appRunner.render_ui(layout)
        )

    def download(self, file: bytes, filename: str) -> None:
        self.__appRunner.scheduler.create_task(
            self.__appRunner.download(file, filename)
        )

    def set_config(self, config: Config) -> None:
        self.__appRunner.scheduler.create_task(self.__appRunner.set_config(config))

    def link(
        self, appRouteOrUrl: str, *, newTab: bool = False, params: Params = {}
    ) -> None:
        """
        Navigate to another Compose App, or link to an external URL.

        If linking to a Compose App, you should define a unique route for the app (`route` param in the App constructor), and then pass that route to this function.

        Furthermore, you can pass a dict of params to the app using the `params` keyword argument. These params will be accessible via `page.params` in the linked app.
        """
        self.__appRunner.scheduler.create_task(
            self.__appRunner.link(appRouteOrUrl, newTab, params)
        )

    def reload(self) -> None:
        """
        Reload the page, which restarts the app.
        """
        self.__appRunner.scheduler.create_task(self.__appRunner.reload())

    def confirm(
        self,
        *,
        title: str = None,
        message: str = None,
        type_to_confirm_text: str = None,
        confirm_button_label: str = None,
        cancel_button_label: str = None,
        appearance: CONFIRM_APPEARANCE = CONFIRM_APPEARANCE_DEFAULT,
    ) -> Awaitable[bool]:
        """
        Display a confirmation dialog to the user.

        Returns a boolean indicating the user's response.
        """
        return self.__appRunner.scheduler.ensure_future(
            self.__appRunner.confirm(
                title=title,
                message=message,
                type_to_confirm_text=type_to_confirm_text,
                confirm_button_label=confirm_button_label,
                cancel_button_label=cancel_button_label,
                appearance=appearance,
            )
        )
