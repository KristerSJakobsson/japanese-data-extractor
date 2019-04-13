# Tests /src/extractor/models/DateValue and /src/extractor/models/ComplexDate

import unittest
from datetime import date

from src.extractor.models.ComplexDate import ComplexDate
from src.extractor.models.DateValue import Year, Month, Day, DateValueType


class TestNumberConvertionUtils(unittest.TestCase):

    def test_is_relative(self):
        day = Day(value=1, type=DateValueType.RELATIVE)

        self.assertTrue(day.is_relative(), f"Expected {day} to be of type relative.")

        day = Day(value=1, type=DateValueType.ABSOLUTE)

        self.assertFalse(day.is_relative(), f"Expected {day} to be of type absolute.")

        month = Month(value=1, type=DateValueType.RELATIVE)

        self.assertTrue(month.is_relative(), f"Expected {month} to be of type relative.")

        month = Month(value=1, type=DateValueType.ABSOLUTE)

        self.assertFalse(month.is_relative(), f"Expected {month} to be of type absolute.")

        year = Year(value=1, type=DateValueType.RELATIVE)

        self.assertTrue(year.is_relative(), f"Expected {year} to be of type relative.")

        year = Year(value=1, type=DateValueType.ABSOLUTE)

        self.assertFalse(year.is_relative(), f"Expected {year} to be of type absolute.")

        complex_date = ComplexDate(year=Year(value=1, type=DateValueType.RELATIVE),
                                   month=Month(value=1, type=DateValueType.ABSOLUTE),
                                   day=Day(value=1, type=DateValueType.ABSOLUTE))

        self.assertTrue(complex_date.is_relative(), f"Expected {complex_date} to be of type relative.")

        complex_date = ComplexDate(year=None,
                                   month=Month(value=1, type=DateValueType.RELATIVE),
                                   day=Day(value=1, type=DateValueType.ABSOLUTE))

        self.assertTrue(complex_date.is_relative(), f"Expected {date} to be of type relative.")

        complex_date = ComplexDate(year=None,
                                   month=None,
                                   day=Day(value=1, type=DateValueType.RELATIVE))

        self.assertTrue(complex_date.is_relative(), f"Expected {date} to be of type relative.")

        complex_date = ComplexDate(year=Year(value=1, type=DateValueType.ABSOLUTE),
                                   month=Month(value=1, type=DateValueType.ABSOLUTE),
                                   day=Day(value=1, type=DateValueType.ABSOLUTE))

        self.assertFalse(complex_date.is_relative(), f"Expected {date} to be of type absolute.")

        complex_date = ComplexDate(year=None,
                                   month=Month(value=1, type=DateValueType.ABSOLUTE),
                                   day=Day(value=1, type=DateValueType.ABSOLUTE))

        self.assertFalse(complex_date.is_relative(), f"Expected {date} to be of type absolute.")

        complex_date = ComplexDate(year=None,
                                   month=None,
                                   day=Day(value=1, type=DateValueType.ABSOLUTE))

        self.assertFalse(complex_date.is_relative(), f"Expected {date} to be of type absolute.")

    def test_convert_to_dateutil_date(self):
        year = 1999
        month = 3
        day = 20

        complex_date = ComplexDate(year=Year(value=year, type=DateValueType.ABSOLUTE),
                                   month=Month(value=month, type=DateValueType.ABSOLUTE),
                                   day=Day(value=day, type=DateValueType.ABSOLUTE))
        converted_complex_date = complex_date.to_dateutil_date()

        dateutil_date = date(year=year, month=month, day=day)

        self.assertEqual(converted_complex_date, dateutil_date,
                         f"Date conversion failed, expected: {dateutil_date} but got: {converted_complex_date}")

        complex_date = ComplexDate(year=Year(value=year, type=DateValueType.ABSOLUTE),
                                   month=Month(value=month, type=DateValueType.ABSOLUTE),
                                   day=Day(value=20, type=DateValueType.RELATIVE))

        relative_dateutil_date = date(year=year, month=2, day=28)  # 20 days before date
        converted_complex_date = complex_date.to_dateutil_date(relative_to=relative_dateutil_date)

        dateutil_date = date(year=year, month=month, day=day)

        self.assertEqual(converted_complex_date, dateutil_date,
                         f"Date conversion failed, expected: {dateutil_date} but got: {converted_complex_date}")

        complex_date = ComplexDate(year=None,
                                   month=Month(value=-12, type=DateValueType.RELATIVE),
                                   day=Day(value=20, type=DateValueType.ABSOLUTE))

        relative_dateutil_date = date(year=year + 1, month=3, day=20)  # 1 year after date
        converted_complex_date = complex_date.to_dateutil_date(relative_to=relative_dateutil_date)

        dateutil_date = date(year=year, month=month, day=day)

        self.assertEqual(converted_complex_date, dateutil_date,
                         f"Date conversion failed, expected: {dateutil_date} but got: {converted_complex_date}")

        complex_date = ComplexDate(year=None,
                                   month=None,
                                   day=Day(value=365, type=DateValueType.RELATIVE))

        relative_dateutil_date = date(year=year - 1, month=3, day=20)  # 1 year before date
        converted_complex_date = complex_date.to_dateutil_date(relative_to=relative_dateutil_date)

        dateutil_date = date(year=year, month=month, day=day)

        self.assertEqual(converted_complex_date, dateutil_date,
                         f"Date conversion failed, expected: {dateutil_date} but got: {converted_complex_date}")
