# Tests /src/extractor/phone_number_extractor

import unittest

from src.extractor.phone_number_extractor import extract_all_phone_numbers


class TestExtract(unittest.TestCase):
    def test_extract_single_phone_number_western_numbers(self):
        string_containing_phone_number = "今の電話番号が「008170-1234-5678」です。"
        extracted_data = extract_all_phone_numbers(target_string=string_containing_phone_number)

        expected_extraction = [((9, 18),
                                {
                                    "phone_number_string": "008170-1234-5678",
                                    "phone_number_value": "00817012345678"
                                })]

        self.assertEqual(extracted_data, expected_extraction,
                         f"Result {extracted_data} is not the same as expectation {expected_extraction}")
    # TODO: Not supported yet
    # def test_extract_single_phone_number_kanji_numbers(self):
    #     string_containing_phone_number = "今の郵便コードが一〇一の二四一二です。"
    #     extracted_data = extract_all_phone_numbers(target_string=string_containing_phone_number)
    #
    #     expected_extraction = [((8, 16),
    #                             {
    #                                 "phone_number_string": "一〇一の二四一二",
    #                                 "phone_number_value": PostalCode("1012412")
    #                             })]
    #
    #     self.assertEqual(extracted_data, expected_extraction,
    #                      f"Result {extracted_data} is not the same as expectation {expected_extraction}")
    #
    # def test_extract_multiple_phone_numbers_mixed_numbers(self):
    #     string_containing_phone_numbers = """"今の郵便コードが二二二の一二一二です。
    #     前の所はT３３３ー３２３２だったし、実家は〒444-1212だった。"""
    #     extracted_data = extract_all_phone_numbers(target_string=string_containing_phone_numbers)
    #
    #     expected_extraction = [((9, 17),
    #                             {
    #                                 "phone_number_string": "二二二の一二一二",
    #                                 "phone_number_value": PostalCode("2221212")
    #                             }),
    #                            ((33, 42),
    #                             {
    #                                 "phone_number_string": "T３３３ー３２３２",
    #                                 "phone_number_value": PostalCode("3333232")
    #                             }),
    #                            ((50, 59),
    #                             {
    #                                 "phone_number_string": "〒444-1212",
    #                                 "phone_number_value": PostalCode("4441212")
    #                             })]
    #
    #     self.assertEqual(extracted_data, expected_extraction,
    #                      f"Result {extracted_data} is not the same as expectation {expected_extraction}")
