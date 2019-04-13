# Tests /src/utils/conversion_utils

import unittest
from typing import Dict, List, Callable, Any

from src.extractor.models.PostalCode import PostalCode
from src.utils.conversion_utils import full_width_string_to_half_width, half_width_string_to_full_width, \
    parse_postal_code


class TestNumberConvertionUtils(unittest.TestCase):

    def verify_each_value_equals_expectation_in_dictionary(self, value_and_expectation: Dict[str, Any],
                                                           verify_function: Callable[[Any], Any]) -> None:
        for string_value in value_and_expectation.keys():
            result = verify_function(string_value)
            expectation = value_and_expectation[string_value]
            self.assertEqual(result, expectation, f'Expected {expectation} but got {result}.')

    def verify_each_value_throws_in_list(self, invalid_numbers: List[str],
                                         verify_function: Callable[[Any], Any]) -> None:
        for numeric_string_value in invalid_numbers:
            with self.assertRaises(ValueError):
                verify_function(numeric_string_value)

    correct_single_digits_and_values_half_width = {str(value): value for value in range(10)}
    correct_single_digits_and_values_full_width = {
        "０": "0",
        "１": "1",
        "２": "2",
        "３": "3",
        "４": "4",
        "５": "5",
        "６": "6",
        "７": "7",
        "８": "8",
        "９": "9"
    }

    def test_full_width_string_to_half_width(self):
        correct_full_width_values = self.correct_single_digits_and_values_full_width
        correct_full_width_values["ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗ"] = "abcdefghijklmnopqrstuvw"

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_full_width_values,
            verify_function=full_width_string_to_half_width)

    def test_half_width_string_to_full_width(self):
        correct_half_width_values = {value: key for key, value in
                                     self.correct_single_digits_and_values_full_width.items()}
        correct_half_width_values["abcdefghijklmnopqrstuvw"] = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗ"

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_half_width_values,
            verify_function=half_width_string_to_full_width)

    def test_parse_postal_code(self):
        postal_codes_and_values = {
            "101-0047": PostalCode("1010047"),
            "１０６-２１５４": PostalCode("1062154"),
            "二〇五の一二四五": PostalCode("2051245"),
            "四〇二之五二四一": PostalCode("4025241")
        }

        invalid_postal_codes = [
            "",
            "文字列",
            "12345678",
            "123456",
            "二〇五ー一二四五"
        ]

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=postal_codes_and_values,
            verify_function=parse_postal_code)
        self.verify_each_value_throws_in_list(
            invalid_numbers=invalid_postal_codes,
            verify_function=parse_postal_code
        )
