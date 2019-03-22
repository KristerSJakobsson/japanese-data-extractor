import regex
from enum import Enum
from typing import Tuple, Any


class NumberType(Enum):
    """
    Enum for Number Types, namely UNIT, MULTIPLE or NUMBER.
    """
    UNIT = 0
    MULTIPLE = 1
    REGULAR = 2
    ZERO = 3


class KanjiNumber(object):
    """
    Container class for Kanji numbers
    """

    def __init__(self, character: str, value: int, number_type: NumberType):
        self.character = character
        self.value = value
        self.number_type = number_type


# Summarize all kanji and relevant information
japanese_number_dict = {
    "〇": KanjiNumber("〇", 0, NumberType.ZERO),
    "零": KanjiNumber("零", 0, NumberType.ZERO),
    "一": KanjiNumber("一", 1, NumberType.REGULAR),
    "二": KanjiNumber("二", 2, NumberType.REGULAR),
    "三": KanjiNumber("三", 3, NumberType.REGULAR),
    "四": KanjiNumber("四", 4, NumberType.REGULAR),
    "五": KanjiNumber("五", 5, NumberType.REGULAR),
    "六": KanjiNumber("六", 6, NumberType.REGULAR),
    "七": KanjiNumber("七", 7, NumberType.REGULAR),
    "八": KanjiNumber("八", 8, NumberType.REGULAR),
    "九": KanjiNumber("九", 9, NumberType.REGULAR),
    "十": KanjiNumber("十", 10, NumberType.UNIT),
    "百": KanjiNumber("百", 100, NumberType.UNIT),
    "千": KanjiNumber("千", 1000, NumberType.UNIT),
    "万": KanjiNumber("万", 10000, NumberType.MULTIPLE),
    "億": KanjiNumber("億", 100000000, NumberType.MULTIPLE),
    "兆": KanjiNumber("兆", 1000000000000, NumberType.MULTIPLE),
    "京": KanjiNumber("京", 10000000000000000, NumberType.MULTIPLE),
    "壱": KanjiNumber("壱", 1, NumberType.REGULAR),
    "弐": KanjiNumber("弐", 2, NumberType.REGULAR),
    "参": KanjiNumber("参", 3, NumberType.REGULAR),
    "拾": KanjiNumber("拾", 10, NumberType.UNIT),
    "萬": KanjiNumber("萬", 10000, NumberType.MULTIPLE)
}

# Note: Currently the dictionary only contains numbers that are acutally used!
japanese_container_dict = {
    "all_numbers": list(japanese_number_dict.keys()),
    "powers_of_ten": [x.character for x in
                      filter((lambda x: x.number_type == NumberType.UNIT or x.number_type == NumberType.MULTIPLE),
                             japanese_number_dict.values())],
    "numbers_multipliers": [x.character for x in
                            filter((lambda x: x.number_type == NumberType.MULTIPLE), japanese_number_dict.values())],
    "0": [x.character for x in filter((lambda x: x.value == 0), japanese_number_dict.values())],
    "0to1": [x.character for x in filter((lambda x: 0 <= x.value <= 1), japanese_number_dict.values())],
    "0to2": [x.character for x in filter((lambda x: 0 <= x.value <= 2), japanese_number_dict.values())],
    "0to4": [x.character for x in filter((lambda x: 0 <= x.value <= 4), japanese_number_dict.values())],
    "0to5": [x.character for x in filter((lambda x: 0 <= x.value <= 5), japanese_number_dict.values())],
    "0to9": [x.character for x in filter((lambda x: 0 <= x.value <= 9), japanese_number_dict.values())],
    "0to10": [x.character for x in filter((lambda x: 0 <= x.value <= 10), japanese_number_dict.values())],
    "0to100": [x.character for x in filter((lambda x: 0 <= x.value <= 100), japanese_number_dict.values())],
    "0to1000": [x.character for x in filter((lambda x: 0 <= x.value <= 1000), japanese_number_dict.values())],
    "1": [x.character for x in filter((lambda x: x.value == 1), japanese_number_dict.values())],
    "1to2": [x.character for x in filter((lambda x: 1 <= x.value <= 2), japanese_number_dict.values())],
    "1to4": [x.character for x in filter((lambda x: 1 <= x.value <= 4), japanese_number_dict.values())],
    "1to5": [x.character for x in filter((lambda x: 1 <= x.value <= 5), japanese_number_dict.values())],
    "1to9": [x.character for x in filter((lambda x: 1 <= x.value <= 9), japanese_number_dict.values())],
    "2": [x.character for x in filter((lambda x: x.value == 2), japanese_number_dict.values())],
    "2to9": [x.character for x in filter((lambda x: 2 <= x.value <= 9), japanese_number_dict.values())],
    "3": [x.character for x in filter((lambda x: x.value == 3), japanese_number_dict.values())],
    "6": [x.character for x in filter((lambda x: x.value == 6), japanese_number_dict.values())],
    "10": [x.character for x in filter((lambda x: x.value == 10), japanese_number_dict.values())],
    "100": [x.character for x in filter((lambda x: x.value == 100), japanese_number_dict.values())]
}


# Note that this function does not take decimal numbers for now!
def mixed_to_value(mixed: str) -> int:
    """
    Converts any dirty number represented with kanji or mixed kanji/numerals to a digit. Dirty mean it may
    contain other characters such as 【,】 etc. These will be ignored in conversion.
    :param mixed: Any dirty digit/kanji string, potentially mixed, such as "２,000億５万五百二十七" or 2,000,000
    :return: The corresponding numerical value
    """

    if mixed is "":
        raise ValueError("Invalid empty string input to the mixed_to_value function.")

    # First, remove anything that is not Kanji numbers or numerals and store cleaned string
    clean_string = ""
    has_kanji_numbers = False

    for char in mixed:
        if char in japanese_container_dict["all_numbers"]:
            clean_string = clean_string + char
            has_kanji_numbers = True
        elif char.isnumeric():
            clean_string = clean_string + char
    if has_kanji_numbers is False:
        # Easy!
        return int(clean_string)
    else:
        return big_number_to_value(clean_string)


def big_number_to_value(kanji_string: str) -> int:
    """
    Converts any clean number represented with kanji or mixed kanji/numerals to a digit.
    Here, clean mean it does not contain any other characters such as "," etc.
    :param kanji_string: Any clean digit/kanji string, potentially mixed, such as "２億５万五百二十七"
    :return: The corresponding numerical value
    """
    # Two cases: Either the kanji_string are western style 二〇〇〇 or Japanese style 二千,
    # we can distinguish these cases using a simple regex that checks if the japanese "powers of ten" are used"

    is_traditional = regex.search(r"\L<japanese_powers_of_ten>", kanji_string,
                                  japanese_powers_of_ten=japanese_container_dict["powers_of_ten"])
    if is_traditional:
        # Japanese style representation of number! We convert by simply multiplying all characters by
        # their corresponding value!
        # Split by multipliers
        final_number = 0
        split = regex.split(r"(\L<japanese_multipliers>)", kanji_string,
                            japanese_multipliers=japanese_container_dict["numbers_multipliers"])
        # Since we capture the splits, the value will be split like: "三百五十万二百"　→ ["三百五十", "万", "二百", ""]
        for iterator in range(0, len(split), 2):
            if split[iterator] is "":
                # If only an multiple is entered, we will have an blank space at the beginning, ignore this!
                continue
            if len(split) is iterator + 1 or split[iterator + 1] is "":
                # Final group between multipliers
                final_number = final_number + string_number_below_ten_thousand_to_value(split[iterator])
            else:
                # Take the value before each multiplier and multiply by the multiplier
                multiplier = japanese_number_dict[split[iterator + 1]].value
                final_number = final_number + string_number_below_ten_thousand_to_value(split[iterator]) * multiplier

        return final_number
    else:
        # No match! Meaning this is a western style representation of a number! We simply convert
        # character by character to western numbers and then parse as integer!
        return western_style_kanji_to_value(kanji_string)


def western_style_kanji_to_value(kanji_string: str) -> int:
    """
    Converts any clean western style kanji number to corresponding digit
    Here, clean mean it does not contain any other characters such as "," etc.
    :param kanji_string: Any western style kanji string, such as "弐〇〇〇"
    :return: The corresponding numerical value
    """
    final_number = ""
    for char in kanji_string:
        final_number = final_number + str(japanese_number_dict[char].value)
    return int(final_number)


def string_number_below_ten_thousand_to_value(numeric_string: str):
    """
    Converts any clean digit (half-width, full-width) and kanji up to 万 (exclusive) to corresponding digit
    Here, clean mean it does not contain any other characters such as "," etc.
    :param numeric_string: Any digit or kanji up to 万 (exclusive)
    :return: A integer transformation of the number
    """
    # Try to convert, if it fails, assume it is a Kanji number
    try:
        # Try converting it with python
        final_numerical_value = int(numeric_string)
    except ValueError:
        # Upon failure, assume it is a Japanese value string
        rest_value = 0
        multiplier_value = 1
        final_numerical_value = 0
        previous_numerical_type = None
        for index, char in enumerate(numeric_string):
            current_numerical_value, current_numerical_type = single_string_digit_to_value(char)

            if current_numerical_type == NumberType.MULTIPLE:
                raise ValueError("Number unexpectedly contained a multiplier above ten thousand")

            if current_numerical_type == NumberType.ZERO and len(numeric_string) > 1:
                raise ValueError("Number unexpectedly contained a zero")

            if current_numerical_type == NumberType.REGULAR and previous_numerical_type == NumberType.REGULAR:
                raise ValueError("Number contained two or more consecutive japanese numbers that were not multipliers")

            if index == len(numeric_string) - 1:
                if current_numerical_type == NumberType.REGULAR:
                    # Save the remainder for the final value, for example 二百五十五 → 5
                    rest_value = current_numerical_value
                elif current_numerical_type == NumberType.UNIT:
                    # Save the remainder for the final value, for example 二百五十 → 0
                    rest_value = 0
            else:
                if current_numerical_type == NumberType.REGULAR:
                    multiplier_value = current_numerical_value
                elif current_numerical_type == NumberType.UNIT:
                    final_numerical_value = final_numerical_value + current_numerical_value * multiplier_value
                    multiplier_value = 1
            previous_numerical_type = current_numerical_type
        final_numerical_value = final_numerical_value + rest_value

    if final_numerical_value < 0:
        raise ValueError(
            "By design, this function should never convert a negative number")

    if final_numerical_value >= 10000:
        raise ValueError(
            "By design, this function should never convert a number equal to or above ten thousand")

    return final_numerical_value


def single_string_digit_to_value(digit: Any) -> Tuple[int, NumberType]:
    if digit in japanese_number_dict.keys():
        input_number = japanese_number_dict[digit]
        return input_number.value, input_number.number_type
    else:
        if digit.isdigit():
            input_number = int(digit)
            if input_number == 0:
                return input_number, NumberType.ZERO
            else:
                return input_number, NumberType.REGULAR
        else:
            raise ValueError("The numeric value could not be interpreted")

#
# def string_number_below_ten_thousand_to_value(numeric_string: str):
#     """
#     Converts any clean digit (half-width, full-width) and kanji up to 万 (exclusive) to corresponding digit
#     Here, clean mean it does not contain any other characters such as "," etc.
#     :param numeric_string: Any digit or kanji up to 万 (exclusive)
#     :return: A integer transformation of the number
#     """
#     # Try to convert, if it fails, assume it is a Kanji number
#     try:
#         # Try converting it with python
#         final_numerical_value = int(numeric_string)
#     except ValueError:
#         # Upon failure, assume it is a Japanese value string
#         working_number = 1  # This acts as both rest and multiplier storage
#         final_numerical_value = 0
#         final_char_is_number = False
#         for char in numeric_string:
#             # Try to interpret the char as a digit (japanese or western)
#             if char in japanese_number_dict.keys():
#                 if japanese_number_dict[char].numbertype is NumberType.NUMBER:
#                     working_number = japanese_number_dict[char].value
#                     final_char_is_number = True
#                 else:  # Multiplier
#                     final_numerical_value = final_numerical_value + japanese_number_dict[char].value * working_number
#                     working_number = 1  # Set next multiplier to 1 by default, 二千百　→　二千一百
#                     final_char_is_number = False
#             else:
#                 if char.isdigit():
#                     working_number = int(char)
#                     final_char_is_number = True
#                 else:
#                     raise ValueError("The numeric string contained a non-numeric value.")
#         else:
#             if final_char_is_number:
#                 rest = working_number  # Save the remainder for the final value, for example 二百五十五 → 5
#             else:
#                 rest = 0  # Save the remainder for the final value, for example 二百五十 → 0
#         final_numerical_value = final_numerical_value + rest
#
#     if final_numerical_value >= 10000:
#         raise ValueError(
#             "By design, the function string_number_below_ten_thousand_to_value should never convert a number equal to or above 10000.")
#
#     return final_numerical_value
