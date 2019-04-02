from enum import Enum


class YearType(Enum):
    RELATIVE = 1
    ABSOLUTE = 2


class Year:
    """
    This model represents a year, either relative or absolute.
    """

    def __init__(self, value: int, type: YearType):
        self.value = value
        self.type = type

    def isRelative(self) -> bool:
        return self.type == YearType.RELATIVE