# Tests /src/execution/analyse

import unittest

from typing import Dict, List

from src.utils.number_convertion_utils import NumberType, single_string_digit_to_value, \
    string_number_below_ten_thousand_to_value

HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000


class TestNumberConvertionUtils(unittest.TestCase):

    def test_single_string_digit_to_value(self):
        def verify_each_value_equals_expectation_in_dictionary(value_and_expectation: Dict[str, int]) -> None:
            for numeric_string_value in value_and_expectation.keys():
                result = single_string_digit_to_value(digit=numeric_string_value)
                expectation_value = value_and_expectation[numeric_string_value]
                expectation_type = NumberType.REGULAR if expectation_value != 0 else NumberType.ZERO
                self.assertEqual(result, (expectation_value, expectation_type),
                                 f'Expected {expectation_value} but got {result}.')

        def verify_each_value_throws_in_list(invalid_numbers: List[str]) -> None:
            for numeric_string_value in invalid_numbers:
                with self.assertRaises(ValueError):
                    single_string_digit_to_value(digit=numeric_string_value)


        correct_single_digits_and_values_half_width = {str(value): value for value in range(10)}
        correct_single_digits_and_values_full_width = {str(value).translate(HALF2FULL): value for value in range(10)}
        correct_single_digits_and_values_kanji = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6,
                                                  "七": 7, "八": 8, "九": 9}
        non_digit_characters = ["a","あ","亜","ア"]

        verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_single_digits_and_values_half_width)
        verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_single_digits_and_values_full_width)
        verify_each_value_equals_expectation_in_dictionary(value_and_expectation=correct_single_digits_and_values_kanji)
        verify_each_value_throws_in_list(invalid_numbers=non_digit_characters)

    def test_string_number_below_ten_thousand_to_value(self):
        def verify_each_value_equals_expectation_in_dictionary(value_and_expectation: Dict[str, int]) -> None:
            for numeric_string_value in value_and_expectation.keys():
                result = string_number_below_ten_thousand_to_value(numeric_string=numeric_string_value)
                expectation = value_and_expectation[numeric_string_value]
                self.assertEqual(result, expectation, f'Expected {expectation} but got {result}.')

        def verify_each_value_throws_in_list(invalid_numbers: List[str]) -> None:
            for numeric_string_value in invalid_numbers:
                with self.assertRaises(ValueError):
                    string_number_below_ten_thousand_to_value(numeric_string=numeric_string_value)

        # Half width numbers
        correct_half_width_numbers_and_correct_values = {
            "0": 0,
            "1": 1,
            "9234": 9234,
            "9999": 9999
        }

        incorrect_half_width_numbers = [
            "10000",
            "-1"
        ]

        verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_half_width_numbers_and_correct_values)
        verify_each_value_throws_in_list(invalid_numbers=incorrect_half_width_numbers)

        # Full width numbers
        full_width_numbers_and_correct_values = {
            "０": 0,
            "１": 1,
            "９２３４": 9234,
            "９９９９": 9999
        }

        incorrect_full_width_numbers = [
            "１００００",
            "-１"
        ]

        verify_each_value_equals_expectation_in_dictionary(value_and_expectation=full_width_numbers_and_correct_values)
        verify_each_value_throws_in_list(invalid_numbers=incorrect_full_width_numbers)

        # Kanji numbers
        kanji_numbers_and_correct_values = {
            "〇": 0,
            "零": 0,
            "一": 1,
            "九千二百三十四": 9234,
            "９千２百３十４": 9234,
            "九千九百九十九": 9999,
            "９千９百９十９": 9999
        }

        incorrect_kanji_numbers = [
            "ゼロ",
            "一万",
            "１万",
            "９九",
            "二百万",
            "百〇一",
            "零一"
        ]

        verify_each_value_equals_expectation_in_dictionary(value_and_expectation=kanji_numbers_and_correct_values)
        verify_each_value_throws_in_list(invalid_numbers=incorrect_kanji_numbers)
