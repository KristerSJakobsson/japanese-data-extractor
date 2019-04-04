# Tests /src/execution/analyse

import unittest
import jsonpickle

from typing import List
from os.path import join

from definitions import TEST_DATA_PATH
from src.downloader.models.DownloadedData import DownloadedData
from src.extractor.postal_code_extractor import extract_all_postal_codes, extract_all_dates
from src.extractor.models.PostalCode import PostalCode
from src.extractor.models.DateValue import Year, Month, Day, DateValueType


class TestExtract(unittest.TestCase):

    @staticmethod
    def _load_test_data() -> List[DownloadedData]:
        input_json_file_name = join(TEST_DATA_PATH, 'test_pages.json')
        with open(input_json_file_name, 'r') as my_file:
            raw_text = my_file.read()
        return jsonpickle.decode(raw_text)

    @staticmethod
    def _dummy_extract_data(data: str) -> str:
        # TODO: Implement this!
        return data

    def test_load_inexistent_file(self):
        test_data = TestExtract._load_test_data()
        test_result = dict()
        for item in test_data:
            test_result[item.title] = TestExtract._dummy_extract_data(item.data)

    def test_extract_single_postal_code_western_numbers(self):
        string_containing_postal_code = "今の郵便コードが「〒012‐2321」です。"
        extracted_data = extract_all_postal_codes(target_string=string_containing_postal_code)

        expected_extraction = [((9, 18),
                                {
                                    "postal_code_string": "〒012‐2321",
                                    "postal_code_value": PostalCode("0122321")
                                })]

        self.assertEqual(extracted_data, expected_extraction,
                         f"Result {extracted_data} is not the same as expectation {expected_extraction}")

    def test_extract_single_postal_code_kanji_numbers(self):
        string_containing_postal_code = "今の郵便コードが一〇一の二四一二です。"
        extracted_data = extract_all_postal_codes(target_string=string_containing_postal_code)

        expected_extraction = [((8, 16),
                                {
                                    "postal_code_string": "一〇一の二四一二",
                                    "postal_code_value": PostalCode("1012412")
                                })]

        self.assertEqual(extracted_data, expected_extraction,
                         f"Result {extracted_data} is not the same as expectation {expected_extraction}")

    def test_extract_multiple_postal_codes_mixed_numbers(self):
        string_containing_postal_codes = """"今の郵便コードが二二二の一二一二です。
        前の所はT３３３ー３２３２だったし、実家は〒444-1212だった。"""
        extracted_data = extract_all_postal_codes(target_string=string_containing_postal_codes)

        expected_extraction = [((9, 17),
                                {
                                    "postal_code_string": "二二二の一二一二",
                                    "postal_code_value": PostalCode("2221212")
                                }),
                               ((33, 42),
                                {
                                    "postal_code_string": "T３３３ー３２３２",
                                    "postal_code_value": PostalCode("3333232")
                                }),
                               ((50, 59),
                                {
                                    "postal_code_string": "〒444-1212",
                                    "postal_code_value": PostalCode("4441212")
                                })]

        self.assertEqual(extracted_data, expected_extraction,
                         f"Result {extracted_data} is not the same as expectation {expected_extraction}")

    def test_extract_single_date_western_numbers(self):
        string_containing_date = "今日は2019-04-03です。"
        extracted_data = extract_all_dates(target_string=string_containing_date)

        expected_extraction = [((3, 13),
                                {
                                    "date_string": "2019-04-03",
                                    "date_year": Year(2019, DateValueType.ABSOLUTE),
                                    "date_month": 4,
                                    "date_day": 3
                                })]

        self.assertEqual(extracted_data, expected_extraction,
                         f"Result {extracted_data} is not the same as expectation {expected_extraction}")

    def test_extract_single_date_kanji_numbers(self):
        string_containing_date = "今日は平成三一年四月三日です。"
        extracted_data = extract_all_dates(target_string=string_containing_date)

        expected_extraction = [((3, 12),
                                {
                                    "date_string": "平成三一年四月三日",
                                    "date_year": Year(2019, DateValueType.ABSOLUTE),
                                    "date_month": 4,
                                    "date_day": 3
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
        for year, relative_value in year_values.items():
            string_containing_date = f"{year}十二月三十一日ではありません。"
            extracted_data = extract_all_dates(target_string=string_containing_date)

            expected_extraction = [((0, 7 + len(year)),
                                    {
                                        "date_string": f"{year}十二月三十一日",
                                        "date_year": Year(relative_value, DateValueType.RELATIVE),
                                        "date_month": Month(12, DateValueType.ABSOLUTE),
                                        "date_day": Day(31, DateValueType.ABSOLUTE)
                                    })]

            self.assertEqual(extracted_data, expected_extraction,
                             f"Result {extracted_data} is not the same as expectation {expected_extraction}")

    def test_extract_single_date_relative_month_kanji(self):
        month_values = {
            -1: "前月",
            0: "今月",
            1: "来月"
        }
        for relative_value, month in month_values.items():
            string_containing_date = f"{month}1日ではありません。"
            extracted_data = extract_all_dates(target_string=string_containing_date)

            expected_extraction = [((0, 4 + len(month)),
                                    {
                                        "date_string": f"{month}1日",
                                        "date_year": None,
                                        "date_month": Month(relative_value, DateValueType.RELATIVE),
                                        "date_day": Day(31, DateValueType.ABSOLUTE)
                                    })]

            self.assertEqual(extracted_data, expected_extraction,
                             f"Result {extracted_data} is not the same as expectation {expected_extraction}")
