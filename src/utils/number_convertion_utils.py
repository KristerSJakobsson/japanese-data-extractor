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


ExtractNumberAndNonnumbersRegex = regex.compile(r"^(?P<numbers>\d*)(?P<nonnumbers>\w*)$")

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
def dirty_mixed_number_to_value(mixed: str) -> int:
    """
    Converts any dirty number represented with kanji or mixed kanji/numerals to a digit. Dirty mean it may
    contain other characters such as comma or other non-numerics. These will be ignored in conversion.
    :param mixed: Any dirty digit/kanji string, potentially mixed, such as "２,000億５万五百二十七" or 2,000,000
    :return: The corresponding numerical value
    """

    if mixed is "":
        raise ValueError("Invalid empty string input to the mixed_to_value function.")

    # First, remove anything that is not Kanji numbers or numerals and store cleaned string
    clean_string = ""

    for char in mixed:
        if char in japanese_container_dict["all_numbers"] or char.isnumeric():
            clean_string = clean_string + char

    return clean_mixed_number_to_value(clean_string)


def clean_mixed_number_to_value(number_string: str) -> int:
    """
    Converts any clean number represented with kanji or mixed kanji/numerals to a digit.
    Here, clean mean it does not contain any other characters such as "," etc.
    :param number_string: Any clean digit/kanji string, potentially mixed, such as "２億５万五百二十七"
    :return: The corresponding numerical value
    """
    # Two cases: Either the kanji_string are western style 二〇〇〇/2000/２０００ or Japanese style 二千/53453百万,
    # we can distinguish these cases using a simple regex that checks if the japanese "powers of ten" are used"

    is_traditional = regex.search(r"\L<japanese_powers_of_ten>", number_string,
                                  japanese_powers_of_ten=japanese_container_dict["powers_of_ten"])
    if is_traditional:
        return traditional_style_kanji_to_value(number_string)
    else:
        try:
            return int(number_string)
        except ValueError:
            return western_style_kanji_to_value(number_string)


def traditional_style_kanji_to_value(kanji_string: str) -> int:
    """
    Converts any clean traditional style kanji number to corresponding digit
    Here, clean mean it does not contain any other characters such as "," etc.
    :param kanji_string: Any traditional style kanji string, such as "二千"
    :return: The corresponding numerical value
    """

    if kanji_string.isdigit():
        raise ValueError(f"Number is a valid number and is thus not a kanji string: {kanji_string}")

    final_number = 0
    split_kanji_by_number_multipliers = regex.split(r"(\L<japanese_multipliers>)",
                                                    kanji_string,
                                                    japanese_multipliers=japanese_container_dict[
                                                        "numbers_multipliers"])
    # Remove blanks from list
    while ("" in split_kanji_by_number_multipliers):
        split_kanji_by_number_multipliers.remove("")

    if len(split_kanji_by_number_multipliers) is 0:
        raise ValueError(f"Number contains no parsable information: {kanji_string}")

    # Since we capture the splits, the value will be split like: "三百五十万二百"　→ ["三百五十", "万", "二百", ""]
    index = 0

    # First we assume that the number might have a western pre-component, like 200万, and thus the base is 1
    base_value = 1
    while index < len(split_kanji_by_number_multipliers):
        selected_value = split_kanji_by_number_multipliers[index]
        for character in selected_value:
            if not character.isdigit() and character not in japanese_container_dict["all_numbers"]:
                raise ValueError(f"Number could not be parsed due to containing \"{character}\": {kanji_string}")

        if selected_value in japanese_container_dict["numbers_multipliers"]:
            # Take the value before each multiplier and multiply by the multiplier
            multiplier_value = japanese_number_dict[selected_value].value
            final_number = final_number + multiplier_value * base_value
            # After the first value, the base will always be 0 unless changed
            base_value = 0
        elif selected_value.isdigit():
            base_value = int(selected_value)
        else:
            number, nonnumber = split_number_and_kanji(selected_value)
            value_of_nonnumber = string_number_below_ten_thousand_to_value(nonnumber)
            if number > value_of_nonnumber:
                # Ex: 47176百
                base_value = number * value_of_nonnumber
            else:
                # Ex: ９千２百３十４
                base_value = string_number_below_ten_thousand_to_value(selected_value)

        index = index + 1

    final_number = final_number + base_value

    return final_number


def split_number_and_kanji(kanji_number: str) -> Tuple[int, str]:
    matches = ExtractNumberAndNonnumbersRegex.search(kanji_number)
    number = matches.group("numbers")
    nonnumber = matches.group("nonnumbers")
    if not number and not nonnumber:
        raise ValueError(f"Number could not be parsed: {kanji_number}")
    return int(number) if number.isdigit() else 1, nonnumber


def western_style_kanji_to_value(kanji_string: str) -> int:
    """
    Converts any clean western style kanji number to corresponding digit
    Here, clean mean it does not contain any other characters such as "," etc.
    :param kanji_string: Any western style kanji string, such as "弐〇〇〇"
    :return: The corresponding numerical value
    """
    try:
        final_number = ""
        for char in kanji_string:
            (number_value, number_type) = parse_single_char_kanji_as_number(kanji=char)
            if number_type in [NumberType.ZERO, NumberType.REGULAR]:
                final_number = final_number + str(number_value)
            else:
                raise ValueError

        return int(final_number)
    except ValueError:
        raise ValueError(f"Failed to parse the string as a western style number: {kanji_string}")


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
            current_numerical_value, current_numerical_type = parse_single_char_digit_as_number(char)

            if current_numerical_type == NumberType.MULTIPLE:
                raise ValueError(f"Number unexpectedly contained a multiplier above ten thousand: {numeric_string}")

            if current_numerical_type == NumberType.ZERO and len(numeric_string) > 1:
                raise ValueError(f"Number unexpectedly contained a zero: {numeric_string}")

            if current_numerical_type == NumberType.REGULAR and previous_numerical_type == NumberType.REGULAR:
                raise ValueError(
                    f"Number contained two or more consecutive japanese numbers that were not multipliers {numeric_string}")

            if index == len(numeric_string) - 1:
                if current_numerical_type == NumberType.REGULAR:
                    # Save the remainder for the final value, for example 二百五十五 → 5
                    rest_value = current_numerical_value
                elif current_numerical_type == NumberType.UNIT:
                    # Save the remainder for the final value, for example 二百五十 → 0
                    rest_value = 0
                    final_numerical_value = final_numerical_value + current_numerical_value * multiplier_value
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
            f"By design, this function should never convert a negative number: {numeric_string}")

    if final_numerical_value >= 10000:
        raise ValueError(
            f"By design, this function should never convert a number equal to or above ten thousand: {numeric_string}")

    return final_numerical_value


def parse_single_char_digit_as_number(digit: Any) -> Tuple[int, NumberType]:
    """
    Parses a single char digit to a numeric value and type
    :param digit: The character to parse (eg. 9、９、九, 百)
    :return: A tuple with the value and NumberType
    """
    try:
        return parse_single_char_kanji_as_number(kanji=digit)
    except ValueError:
        if digit.isdigit():
            input_number = int(digit)
            if input_number == 0:
                return input_number, NumberType.ZERO
            else:
                return input_number, NumberType.REGULAR
        else:
            raise ValueError(
                f"The numeric value could not be interpreted as either a kanji number or normal number: {digit}")


def parse_single_char_kanji_as_number(kanji: Any) -> Tuple[int, NumberType]:
    """
    Parses a single char kanji to a numeric value and type
    :param kanji: The kanji to parse (eg. 九, 百)
    :return: A tuple with the value and NumberType
    """
    if kanji in japanese_number_dict.keys():
        input_number = japanese_number_dict[kanji]
        return input_number.value, input_number.number_type
    else:
        raise ValueError(f"The numeric value could not be interpreted as a kanji number: {kanji}")
