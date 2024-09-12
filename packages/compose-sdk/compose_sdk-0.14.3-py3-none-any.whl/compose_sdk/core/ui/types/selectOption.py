from typing import TypedDict
from typing_extensions import NotRequired

SelectOptionValue = str | int


class SelectOptionDict(TypedDict):
    value: SelectOptionValue
    label: str
    description: NotRequired[str]


SelectOptionPrimitive = SelectOptionValue

SelectOptions = list[SelectOptionDict] | list[SelectOptionPrimitive]
