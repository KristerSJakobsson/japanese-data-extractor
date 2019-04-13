# Tests /src/execution/analyse

import unittest

from src.extractor.models.PostalCode import PostalCode
from src.extractor.postal_code_extractor import extract_all_postal_codes


class TestExtract(unittest.TestCase):
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
