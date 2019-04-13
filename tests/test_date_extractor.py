# Tests /src/execution/analyse

import unittest

from src.extractor.models.DateValue import Year, Month, Day, DateValueType
from src.extractor.models.ComplexDate import ComplexDate
from src.extractor.date_extractor import extract_all_dates


class TestExtract(unittest.TestCase):

    def test_extract_single_date_western_numbers(self):
        string_containing_date = "今日は2019-04-03です。"
        extracted_data = extract_all_dates(target_string=string_containing_date)

        year = Year(2019, DateValueType.ABSOLUTE)
        month = Month(4, DateValueType.ABSOLUTE)
        day = Day(3, DateValueType.ABSOLUTE)

        expected_extraction = [((3, 13),
                                {
                                    "date_string": "2019-04-03",
                                    "date_year": year,
                                    "date_month": month,
                                    "date_day": day,
                                    "date": ComplexDate(year=year, month=month, day=day)
                                })]

        self.assertEqual(extracted_data, expected_extraction,
                         f"Result {extracted_data} is not the same as expectation {expected_extraction}")

    def test_extract_single_date_kanji_numbers(self):
        string_containing_date = "今日は平成三一年四月三日です。"
        extracted_data = extract_all_dates(target_string=string_containing_date)

        year = Year(2019, DateValueType.ABSOLUTE)
        month = Month(4, DateValueType.ABSOLUTE)
        day = Day(3, DateValueType.ABSOLUTE)

        expected_extraction = [((3, 12),
                                {
                                    "date_string": "平成三一年四月三日",
                                    "date_year": year,
                                    "date_month": month,
                                    "date_day": day,
                                    "date": ComplexDate(year=year, month=month, day=day)
                                })]

        self.assertEqual(extracted_data, expected_extraction,
                         f"Result {extracted_data} is not the same as expectation {expected_extraction}")

    def test_extract_single_date_relative_years_kanji(self):
        year_values = {
            "去年": -1,
            "今年": 0,
            "本年": 0,
            "来年": 1,
            "再来年": 2
        }

        month = Month(12, DateValueType.ABSOLUTE)
        day = Day(31, DateValueType.ABSOLUTE)

        for relative_year, relative_value in year_values.items():
            string_containing_date = f"次は{relative_year}十二月三十一日ではありません。"
            extracted_data = extract_all_dates(target_string=string_containing_date)

            year = Year(relative_value, DateValueType.RELATIVE)

            expected_extraction = [((2, 9 + len(relative_year)),
                                    {
                                        "date_string": f"{relative_year}十二月三十一日",
                                        "date_year": year,
                                        "date_month": month,
                                        "date_day": day,
                                        "date": ComplexDate(year=year, month=month, day=day)
                                    })]

            self.assertEqual(extracted_data, expected_extraction,
                             f"Result {extracted_data} is not the same as expectation {expected_extraction}")

    def test_extract_single_date_relative_month_kanji(self):
        month_values = {
            "前月": -1,
            "今月": 0,
            "来月": 1
        }

        year = None
        day = Day(1, DateValueType.ABSOLUTE)

        for relative_month, relative_value in month_values.items():
            string_containing_date = f"次は{relative_month}1日ではありません。"
            extracted_data = extract_all_dates(target_string=string_containing_date)

            month = Month(relative_value, DateValueType.RELATIVE)

            expected_extraction = [((2, 4 + len(relative_month)),
                                    {
                                        "date_string": f"{relative_month}1日",
                                        "date_year": year,
                                        "date_month": month,
                                        "date_day": day,
                                        "date": ComplexDate(year=year, month=month, day=day)
                                    })]

            self.assertEqual(extracted_data, expected_extraction,
                             f"Result {extracted_data} is not the same as expectation {expected_extraction}")


    # TODO: Currently this is not supported
    # def test_extract_single_date_relative_day_kanji(self):
    #     day_values = {
    #         "一昨日": -2,
    #         "昨日": -1,
    #         "今日": 0,
    #         "本日": 0,
    #         "明日": 1,
    #         "明後日": 2
    #     }
    #
    #     year = None
    #     month = None
    #
    #     for relative_day, relative_value in day_values.items():
    #         string_containing_date = f"次は{relative_day}ではありません。"
    #         extracted_data = extract_all_dates(target_string=string_containing_date)
    #
    #         day = Day(relative_value, DateValueType.RELATIVE)
    #
    #         expected_extraction = [((2, 2 + len(relative_day)),
    #                                 {
    #                                     "date_string": f"{relative_day}",
    #                                     "date_year": year,
    #                                     "date_month": month,
    #                                     "date_day": day,
    #                                     "date": ComplexDate(year=year, month=month, day=day)
    #                                 })]
    #
    #         self.assertEqual(extracted_data, expected_extraction,
    #                          f"Result {extracted_data} is not the same as expectation {expected_extraction}")
