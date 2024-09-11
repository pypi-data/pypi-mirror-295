from typing import Literal

LAYOUT_DIRECTION = Literal[
    "vertical",
    "vertical-reverse",
    "horizontal",
    "horizontal-reverse",
]

LAYOUT_DIRECTION_DEFAULT: LAYOUT_DIRECTION = "vertical"

LAYOUT_JUSTIFY = Literal[
    "start",
    "end",
    "center",
    "between",
    "around",
    "evenly",
]

LAYOUT_JUSTIFY_DEFAULT: LAYOUT_JUSTIFY = "start"

LAYOUT_ALIGN = Literal[
    "start",
    "end",
    "center",
    "baseline",
    "stretch",
]

LAYOUT_ALIGN_DEFAULT: LAYOUT_ALIGN = "start"
