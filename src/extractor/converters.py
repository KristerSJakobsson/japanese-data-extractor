import regex
from enum import Enum

class NumberType(Enum):
    """
    Enum for Number Types, namely UNIT, MULTIPLE or NUMBER.
    """
    UNIT = 0
    MULTIPLE = 1
    NUMBER = 2


class KanjiNumber(object):
    """
    Container class for Kanji numbers
    """
    def __init__(self, character: str, value: int, numbertype: NumberType):
        self.character = character
        self.value = value
        self.numbertype = numbertype

# Summarize all kanji and relevant information
kanji_number_dict = {
    "〇":KanjiNumber("〇", 0, NumberType.NUMBER),
    "零":KanjiNumber("零", 0, NumberType.NUMBER),
    "一":KanjiNumber("一", 1, NumberType.NUMBER),
    "二":KanjiNumber("二", 2, NumberType.NUMBER),
    "三":KanjiNumber("三", 3, NumberType.NUMBER),
    "四":KanjiNumber("四", 4, NumberType.NUMBER),
    "五":KanjiNumber("五", 5, NumberType.NUMBER),
    "六":KanjiNumber("六", 6, NumberType.NUMBER),
    "七":KanjiNumber("七", 7, NumberType.NUMBER),
    "八":KanjiNumber("八", 8, NumberType.NUMBER),
    "九":KanjiNumber("九", 9, NumberType.NUMBER),
    "十":KanjiNumber("十", 10, NumberType.UNIT),
    "百":KanjiNumber("百", 100, NumberType.UNIT),
    "千":KanjiNumber("千", 1000, NumberType.UNIT),
    "万":KanjiNumber("万", 10000, NumberType.MULTIPLE),
    "億":KanjiNumber("億", 100000000, NumberType.MULTIPLE),
    "兆":KanjiNumber("兆", 1000000000000, NumberType.MULTIPLE),
    "京":KanjiNumber("京", 10000000000000000, NumberType.MULTIPLE),
    "壱":KanjiNumber("壱", 1, NumberType.NUMBER),
    "弐":KanjiNumber("弐", 2, NumberType.NUMBER),
    "参":KanjiNumber("参", 3, NumberType.NUMBER),
    "拾":KanjiNumber("拾", 10, NumberType.UNIT),
    "萬": KanjiNumber("萬", 10000, NumberType.MULTIPLE)
}

# Note: Currently the dictionary only contains numbers that are acutally used!
kanji_container_dict = {
    "all_numbers":list(kanji_number_dict.keys()),
    "powers_of_ten":[x.character for x in filter((lambda x: x.numbertype == NumberType.UNIT or x.numbertype == NumberType.MULTIPLE), kanji_number_dict.values())],
    "numbers_multipliers":[x.character for x in filter((lambda x: x.numbertype == NumberType.MULTIPLE), kanji_number_dict.values())],
    "0":[x.character for x in filter((lambda x: x.value == 0), kanji_number_dict.values())],
    "0to1":[x.character for x in filter((lambda x: 0 <= x.value <= 1), kanji_number_dict.values())],
    "0to2":[x.character for x in filter((lambda x: 0 <= x.value <= 2), kanji_number_dict.values())],
    "0to4":[x.character for x in filter((lambda x: 0 <= x.value <= 4), kanji_number_dict.values())],
    "0to5":[x.character for x in filter((lambda x: 0 <= x.value <= 5), kanji_number_dict.values())],
    "0to9":[x.character for x in filter((lambda x: 0 <= x.value <= 9), kanji_number_dict.values())],
    "0to10":[x.character for x in filter((lambda x: 0 <= x.value <= 10), kanji_number_dict.values())],
    "0to100":[x.character for x in filter((lambda x: 0 <= x.value <= 100), kanji_number_dict.values())],
    "0to1000":[x.character for x in filter((lambda x: 0 <= x.value <= 1000), kanji_number_dict.values())],
    "1":[x.character for x in filter((lambda x: x.value == 1), kanji_number_dict.values())],
    "1to2":[x.character for x in filter((lambda x: 1 <= x.value  <= 2), kanji_number_dict.values())],
    "1to4":[x.character for x in filter((lambda x: 1 <= x.value  <= 4), kanji_number_dict.values())],
    "1to5":[x.character for x in filter((lambda x: 1 <= x.value  <= 5), kanji_number_dict.values())],
    "1to9":[x.character for x in filter((lambda x: 1 <= x.value <= 9), kanji_number_dict.values())],
    "2":[x.character for x in filter((lambda x: x.value == 2), kanji_number_dict.values())],
    "2to9":[x.character for x in filter((lambda x: 2 <= x.value <= 9), kanji_number_dict.values())],
    "3":[x.character for x in filter((lambda x: x.value == 3), kanji_number_dict.values())],
    "6":[x.character for x in filter((lambda x: x.value == 6), kanji_number_dict.values())],
    "10":[x.character for x in filter((lambda x: x.value == 10), kanji_number_dict.values())],
    "100":[x.character for x in filter((lambda x: x.value == 100), kanji_number_dict.values())]
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
        if char in kanji_container_dict["all_numbers"]:
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
    Converts any clean number represented with kanji or mixed kanji/numerals to a digit. Clean mean it does not
    contain any other characters such as 【,】 etc.
    :param kanji_string: Any clean digit/kanji string, potentially mixed, such as "２億５万五百二十七"
    :return: The corresponding numerical value
    """
    # Two cases: Either the kanji_string are western style 二〇〇〇 or Japanese style 二千,
    # we can distinguish these cases using a simple regex that checks if the japanese "powers of ten" are used"


    is_traditional = regex.search(r"\L<japanese_powers_of_ten>", kanji_string, japanese_powers_of_ten=kanji_container_dict["powers_of_ten"])
    if is_traditional:
        # Japanese style representation of number! We convert by simply multiplying all characters by
        # their corresponding value!
        # Split by multipliers
        final_number = 0
        split = regex.split(r"(\L<japanese_multipliers>)", kanji_string, japanese_multipliers=kanji_container_dict["numbers_multipliers"])
        # Since we capture the splits, the value will be split like: "三百五十万二百"　→ ["三百五十", "万", "二百", ""]
        for iterator in range(0, len(split), 2):
            if split[iterator] is "":
                # If only an multiple is entered, we will have an blank space at the beginning, ignore this!
                continue
            if len(split) is iterator+1 or split[iterator + 1] is "":
                # Final group between multipliers
                final_number = final_number + small_number_to_value(split[iterator])
            else:
                # Take the value before each multiplier and multiply by the multiplier
                final_number = final_number + small_number_to_value(split[iterator]) * kanji_number_dict[split[iterator + 1]].value


        return final_number
    else:
        # No match! Meaning this is a western style representation of a number! We simply convert
        # character by character to western numbers and then parse as integer!
        return western_style_kanji_to_value(kanji_string)

def western_style_kanji_to_value(kanji_string: str) -> int:
    """
    Converts any western style kanji number to corresponding digit
    :param kanji_string: Any western style kanji string, such as "弐〇〇〇"
    :return: The corresponding numerical value
    """
    final_number = ""
    for char in kanji_string:
        final_number = final_number + str(kanji_number_dict[char].value)
    return int(final_number)


def small_number_to_value(numeric_string: str):
    """
    Converts any digit (half-width, full-width) and kanji up to 万 (exclusive) to corresponding digit
    :param numeric_string: Any digit or kanji up to 万 (exclusive)
    :return: A integer transformation of the number
    """
    # Try to convert, if it fails, assume it is a Kanji number
    try:
        # Try converting it with python
        value = int(numeric_string)
    except ValueError:
        # Upon failure, assume it is a Japanese value string
        number = 1 # In case no numeber is defined, default
        value = 0
        final_char_is_number = False
        for char in numeric_string:
            if kanji_number_dict[char].numbertype is NumberType.NUMBER:
                number = kanji_number_dict[char].value
                final_char_is_number = True
            else: # Multiplier
                value = value + kanji_number_dict[char].value * number
                number = 1 # Set next multiplier to 1 by default, 二千百　→　二千一百
                final_char_is_number = False
        else:
            if final_char_is_number:
                rest = number  # Save the remaining final value, for example 二百五十五 → 5
            else:
                rest = 0 # Save the remaining final value, for example 二百五十 → 0
        value = value + rest
    return value
