from datetime import date
from typing import Optional

from dateutil.relativedelta import relativedelta

from .DateValue import Year, Month, Day


class ComplexDate:

    def __init__(self, year: Optional[Year], month: Optional[Month], day: Optional[Day]):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return f"Year: {self.year}, Month: {self.month}, Day: {self.day}"

    def __eq__(self, other: Optional['ComplexDate']) -> bool:
        if other is None:
            return False

        equal = self.year == other.year and self.month == other.month and self.day == other.day
        return equal

    def is_relative(self):
        if self.day and self.day.is_relative():
            return True

        if self.month and self.month.is_relative():
            return True

        if self.year and self.year.is_relative():
            return True

        return False

    def to_dateutil_date(self, relative_to: Optional[date] = date.today()) -> date:

        if self.day:
            if self.day.is_relative():
                delta = relativedelta(days=self.day.value)
                return relative_to + delta
            else:
                day = self.day.value
        else:
            raise ValueError(f"Not possible to parse date: {self}")

        if self.month:
            if self.month.is_relative():
                delta = relativedelta(months=self.month.value)
                relative_date_without_day = relative_to + delta
                return relative_date_without_day.replace(day=day)
            else:
                month = self.month.value
        else:
            raise ValueError(f"Not possible to parse date: {self}")

        if self.year:
            if self.year.is_relative():
                delta = relativedelta(years=self.year.value)
                relative_date_without_month_and_day = relative_to + delta
                return relative_date_without_month_and_day.replace(month=month, day=day)
            else:
                year = self.year.value
        else:
            raise ValueError(f"Not possible to parse date: {self}")

        return date(year=year, month=month, day=day)
