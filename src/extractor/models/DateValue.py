from abc import ABC
from enum import Enum
from typing import Optional


class DateValueType(Enum):
    RELATIVE = 1
    ABSOLUTE = 2


class DateValue(ABC):
    """
    This model represents a date value, either relative or absolute.
    """

    def __init__(self, value: int, type: DateValueType):
        self.value = value
        self.type = type

    def is_relative(self) -> bool:
        return self.type == DateValueType.RELATIVE

    @staticmethod
    def compare(this: 'DateValue', other: Optional['DateValue']):
        if other is None:
            return False

        if this.value == other.value and \
                this.type == other.type:
            return True

        return False


class Year(DateValue):
    def __eq__(self, other: Optional['Year']) -> bool:
        return DateValue.compare(self, other)


class Month(DateValue):
    def __eq__(self, other: Optional['Month']) -> bool:
        return DateValue.compare(self, other)


class Day(DateValue):
    def __eq__(self, other: Optional['Day']) -> bool:
        return DateValue.compare(self, other)
