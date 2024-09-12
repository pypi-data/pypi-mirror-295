from typing import Union
from ..ui import (
    INTERACTION_TYPE,
    TYPE,
    Nullable,
    LAYOUT_ALIGN,
    LAYOUT_DIRECTION,
    LAYOUT_JUSTIFY,
    LAYOUT_ALIGN_DEFAULT,
    LAYOUT_DIRECTION_DEFAULT,
    LAYOUT_JUSTIFY_DEFAULT,
    ComponentReturn,
)
from ..utils import Utils

Children = Union[ComponentReturn, list[ComponentReturn]]


def layout_stack(
    children: Children,
    *,
    direction: LAYOUT_DIRECTION = LAYOUT_DIRECTION_DEFAULT,
    justify: LAYOUT_JUSTIFY = LAYOUT_JUSTIFY_DEFAULT,
    align: LAYOUT_ALIGN = LAYOUT_ALIGN_DEFAULT,
    style: Nullable.Style = None
) -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "children": children,
            "direction": direction,
            "justify": justify,
            "align": align,
            "style": style,
            "properties": {},
        },
        "hooks": None,
        "type": TYPE.LAYOUT_STACK,
        "interactionType": INTERACTION_TYPE.LAYOUT,
    }


def layout_form(
    id: str,
    children: Children,
    *,
    direction: LAYOUT_DIRECTION = LAYOUT_DIRECTION_DEFAULT,
    justify: LAYOUT_JUSTIFY = LAYOUT_JUSTIFY_DEFAULT,
    align: LAYOUT_ALIGN = LAYOUT_ALIGN_DEFAULT,
    style: Nullable.Style = None,
    clear_on_submit: bool = False,
    validate: Nullable.Callable = None,
    on_submit: Nullable.Callable = None
) -> ComponentReturn:
    return {
        "model": {
            "id": id,
            "children": children,
            "direction": direction,
            "justify": justify,
            "align": align,
            "style": style,
            "properties": {
                "hasOnSubmitHook": on_submit is not None,
                "hasValidateHook": validate is not None,
                "clearOnSubmit": clear_on_submit,
            },
        },
        "hooks": {
            "validate": validate,
            "onSubmit": on_submit,
        },
        "type": TYPE.LAYOUT_FORM,
        "interactionType": INTERACTION_TYPE.LAYOUT,
    }
