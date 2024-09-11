from typing import Callable, Dict, Literal, Union, TypedDict
from typing_extensions import NotRequired
from datetime import datetime

TABLE_COLUMN_FORMAT = Literal[
    # 10/14
    "DATE_SHORT",
    # 10/14/1983
    "DATE_SHORT_WITH_YEAR",
    # Oct 14
    "DATE_MED",
    # Oct 14, 1983
    "DATE_MED_WITH_YEAR",
    # 10:14 AM
    "TIME_SHORT",
    # 10:14 AM EDT
    "TIME_SHORT_WITH_OFFSET",
    # 10/14/1983, 10:14 AM
    "DATETIME_SHORT",
    # Oct 14, 1983, 10:14 AM
    "DATETIME_MED",
    # 10/14/1983, 10:14 AM EDT
    "DATETIME_SHORT_WITH_OFFSET",
    # Oct 14, 1983, 10:14 AM EDT
    "DATETIME_MED_WITH_OFFSET",
    # $1000.00
    "CURRENCY",
    # $1,000
    "CURRENCY_ROUNDED",
    # 1,234
    "NUMBER_ROUNDED",
]


class TableColumn(TypedDict):
    label: str
    key: str
    format: NotRequired[TABLE_COLUMN_FORMAT]
    width: NotRequired[str]


TableColumns = list[TableColumn]

TableDataRow = Dict[str, Union[str, int, float, datetime, None]]
TableData = list[TableDataRow]


class TableActionWithoutOnClick(TypedDict):
    label: str
    surface: NotRequired[bool]


class TableAction(TableActionWithoutOnClick):
    on_click: Callable[[TableDataRow], None]


TableActionOnClick = TableAction["on_click"]

TableActions = list[TableAction]
TableActionsWithoutOnClick = list[TableActionWithoutOnClick]
TableActionsOnClick = list[TableActionOnClick]
