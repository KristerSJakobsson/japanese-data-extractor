# Tests /src/utils/number_conversion_utils

import unittest
from typing import Dict, List, Callable, Any

from src.utils.number_conversion_utils import parse_single_char_digit_as_number, \
    string_number_below_ten_thousand_to_value, traditional_style_kanji_to_value, western_style_kanji_to_value, \
    clean_mixed_number_to_value, dirty_mixed_number_to_value

HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000


class TestNumberConvertionUtils(unittest.TestCase):

    def verify_each_value_equals_expectation_in_dictionary(self, value_and_expectation: Dict[str, int],
                                                           verify_function: Callable[[Any], int]) -> None:
        for numeric_string_value in value_and_expectation.keys():
            result = verify_function(numeric_string_value)
            expectation = value_and_expectation[numeric_string_value]
            self.assertEqual(result, expectation, f'Expected {expectation} but got {result}.')

    def verify_each_value_throws_in_list(self, invalid_numbers: List[str],
                                         verify_function: Callable[[Any], int]) -> None:
        for numeric_string_value in invalid_numbers:
            with self.assertRaises(ValueError):
                verify_function(numeric_string_value)

    def test_parse_single_char_digit_as_number(self):
        correct_single_digits_and_values_half_width = {str(value): value for value in range(10)}
        correct_single_digits_and_values_full_width = {str(value).translate(HALF2FULL): value for value in range(10)}
        correct_single_digits_and_values_kanji = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6,
                                                  "七": 7, "八": 8, "九": 9}
        non_digit_characters = ["a", "あ", "亜", "ア"]

        def parse_single_char_digit_as_number_and_return_number(digit: Any) -> int:
            number = parse_single_char_digit_as_number(digit=digit)
            return number.value

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_single_digits_and_values_half_width,
            verify_function=parse_single_char_digit_as_number_and_return_number)
        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_single_digits_and_values_full_width,
            verify_function=parse_single_char_digit_as_number_and_return_number)
        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_single_digits_and_values_kanji,
            verify_function=parse_single_char_digit_as_number_and_return_number)
        self.verify_each_value_throws_in_list(
            invalid_numbers=non_digit_characters,
            verify_function=parse_single_char_digit_as_number_and_return_number)

    def test_string_number_below_ten_thousand_to_value(self):

        # Half width numbers
        correct_half_width_numbers_and_correct_values = {
            "0": 0,
            "1": 1,
            "9234": 9234,
            "9999": 9999
        }

        incorrect_half_width_numbers = [
            "10000",
            "-1",
            "文字列"
        ]

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_half_width_numbers_and_correct_values,
            verify_function=string_number_below_ten_thousand_to_value)
        self.verify_each_value_throws_in_list(
            invalid_numbers=incorrect_half_width_numbers,
            verify_function=string_number_below_ten_thousand_to_value)

        # Full width numbers
        full_width_numbers_and_correct_values = {
            "０": 0,
            "１": 1,
            "９２３４": 9234,
            "９９９９": 9999
        }

        incorrect_full_width_numbers = [
            "１００００",
            "-１",
            "文字列"
        ]

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=full_width_numbers_and_correct_values,
            verify_function=string_number_below_ten_thousand_to_value)
        self.verify_each_value_throws_in_list(
            invalid_numbers=incorrect_full_width_numbers,
            verify_function=string_number_below_ten_thousand_to_value)

        # Kanji numbers
        kanji_numbers_and_correct_values = {
            "〇": 0,
            "零": 0,
            "一": 1,
            "弐": 2,
            "十": 10,
            "二百": 200,
            "六十": 60,
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
            "零一",
            "文字列"
        ]

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=kanji_numbers_and_correct_values,
            verify_function=string_number_below_ten_thousand_to_value)
        self.verify_each_value_throws_in_list(
            invalid_numbers=incorrect_kanji_numbers,
            verify_function=string_number_below_ten_thousand_to_value)

    def test_traditional_style_kanji_to_value(self):

        correct_traditional_style_kanji_numbers = {
            "〇": 0,
            "零": 0,
            "一": 1,
            "弐": 2,
            "十": 10,
            "二百": 200,
            "六十": 60,
            "二百万": 2000000,
            "九千二百三十四": 9234,
            "９千２百３十４": 9234,
            "九千九百九十九": 9999,
            "９千９百９十９": 9999
        }

        incorrect_traditional_style_kanji_numbers = [
            "一九九九",
            "九九九九九九",
            "一二三四五六",
            "弐〇〇〇",
            "1999"
            "９９９９９９",
            "123456",
            "",
            "ゼロ",
            "９九",
            "文字列"
        ]

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_traditional_style_kanji_numbers,
            verify_function=traditional_style_kanji_to_value
        )
        self.verify_each_value_throws_in_list(
            invalid_numbers=incorrect_traditional_style_kanji_numbers,
            verify_function=traditional_style_kanji_to_value
        )

    def test_western_style_kanji_to_value(self):

        correct_western_style_kanji_numbers = {
            "〇": 0,
            "零": 0,
            "一": 1,
            "弐": 2,
            "一〇": 10,
            "一九九九": 1999,
            "九九九九九九": 999999,
            "一二三四五六": 123456,
            "弐〇〇〇": 2000
        }

        incorrect_western_style_kanji_numbers = [
            "十",
            "1999",
            "９９９９９９",
            "123456",
            "",
            "ゼロ",
            "９九",
            "二百万",
            "文字列"
        ]

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_western_style_kanji_numbers,
            verify_function=western_style_kanji_to_value
        )
        self.verify_each_value_throws_in_list(
            invalid_numbers=incorrect_western_style_kanji_numbers,
            verify_function=western_style_kanji_to_value
        )

    def test_clean_mixed_number_to_value(self):
        correct_clean_mixed_numbers_and_values = {
            "一九九九": 1999,
            "九九九九九九": 999999,
            "一二三四五六": 123456,
            "弐〇〇〇": 2000,
            "1999": 1999,
            "９９９９９９": 999999,
            "123456": 123456,
            "二百万": 2000000,
            "200万": 2000000,
            "47176百万": 47176000000
        }

        incorrect_clean_mixed_numbers = [
            "",
            "ゼロ",
            "９九",
            "文字列"
        ]

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_clean_mixed_numbers_and_values,
            verify_function=clean_mixed_number_to_value
        )
        self.verify_each_value_throws_in_list(
            invalid_numbers=incorrect_clean_mixed_numbers,
            verify_function=clean_mixed_number_to_value
        )

    def test_dirty_mixed_number_to_value(self):
        correct_dirty_mixed_numbers_and_values = {
            "文字列一九九九文字列": 1999,
            "九九九、九九九": 999999,
            "一二三ゴミ四五六": 123456,
            "1999年": 1999,
            "９９９、９９９": 999999,
            "123,456": 123456,
            "JPY47,176百万": 47176000000,
            "２,000億５万五百二十七": 200000050527
        }

        incorrect_dirty_mixed_numbers = [
            "",
            "ゼロ",
            "９九",
            "文字列"
        ]

        self.verify_each_value_equals_expectation_in_dictionary(
            value_and_expectation=correct_dirty_mixed_numbers_and_values,
            verify_function=dirty_mixed_number_to_value
        )
        self.verify_each_value_throws_in_list(
            invalid_numbers=incorrect_dirty_mixed_numbers,
            verify_function=dirty_mixed_number_to_value
        )
