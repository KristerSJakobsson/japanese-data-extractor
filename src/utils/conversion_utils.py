from typing import Optional
from collections import namedtuple

from src.utils.number_conversion_utils import western_style_kanji_to_value
from src.extractor.models.PostalCode import PostalCode
from src.extractor.models.Year import Year, YearType

from src.extractor.constants import prefixes
from src.utils.number_conversion_utils import dirty_mixed_number_to_value

HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000

FULL2HALF = dict((i + 0xFEE0, i) for i in range(0x21, 0x7F))
FULL2HALF[0x3000] = 0x20

POSTAL_CODE_JAPANESE_SEPARATORS = ["の", "ノ", "之", "ﾉ"]

Era = namedtuple('Era', ['gregorian_calendar_offset', 'length_in_years'])
JAPANESE_ERAS = {
    "大正": Era(1911, 15),
    "昭和": Era(1925, 64),
    "平成": Era(1988, 31),
    "令和": Era(1912, None)
}


def full_width_string_to_half_width(full_width_string: str) -> str:
    """
    Convert full-width characters to half-width counterpart
    :param full_width_string: Some full-width string
    :return: Corresponding half-width string
    """
    return full_width_string.translate(FULL2HALF)


def half_width_string_to_full_width(half_width_string: str) -> str:
    """
    Convert half-width characters to full-width counterpart
    :param half_width_string: Some half-width string
    :return: Corresponding full-width string
    """
    return half_width_string.translate(HALF2FULL)


def parse_postal_code(postal_code: str) -> PostalCode:
    """
    Function used to convert postal code to default model
    :param postal_code: Some postal code, possibly formatted with kanji or full-width numbers
    :return: Correctly formatted postal code nnn-nnnn
    """
    converted_code = ""
    for japanese_separator in POSTAL_CODE_JAPANESE_SEPARATORS:
        if japanese_separator in postal_code:
            # Assume it's a japanese number
            pieces = postal_code.split(japanese_separator)
            converted_code = f"{western_style_kanji_to_value(pieces[0])}{western_style_kanji_to_value(pieces[1])}"
            break
    else:
        # Assume it's not a japanese number, contains only numbers and seperator
        for char in postal_code:
            if char.isnumeric():
                # Conversion turns full-width characters to half-width
                converted_code = converted_code + full_width_string_to_half_width(char)

    return PostalCode.from_string(postal_code=converted_code)


def parse_relative_year_value(relative_year: str) -> int:
    """
    Parses a relative year value such as "去年"
    :param relative_year: The year to parse
    :return: An integer representing the relative value of the year, for example -1
    """
    if relative_year == "去年":
        return -1
    if relative_year == "今年" or relative_year == "本年":
        return 0
    if relative_year == "来年":
        return 1
    if relative_year == "再来年":
        return 2
    raise ValueError(f"Could not parse the input as a relative year: {relative_year}")


def parse_japanese_year_value(japanese_year: str) -> int:
    """
    Parses an absolute year value such as "昭和63"
    :param japanese_year: The year to parse
    :return: An integer representing the absolute value of the year, for example 1988
    """
    for era_name, era_details in JAPANESE_ERAS.items():
        if japanese_year[0:2] == era_name:
            relative_year = dirty_mixed_number_to_value(japanese_year[2:])
            if relative_year < 1 or (era_details.length_in_years and relative_year > era_details.length_in_years):
                raise ValueError(
                    f"The {era_name} era needs to have a number between 1 and {era_details.length_in_years}: {japanese_year}")
            return era_details.gregorian_calendar_offset + relative_year
    raise ValueError(f"Could not parse the input as a Japanese year: {japanese_year}")


def parse_year(year: str) -> Optional[Year]:
    """
    Function used to contain year (relative or fixed) to a number
    :param year: Either a year or a relative year
    :return: Either a fixed year or a relative year
    """

    if not year:
        return None
    for japanese_year_prefix in prefixes["date_japanese_year"]:
        if year.startswith(japanese_year_prefix):
            return Year(parse_japanese_year_value(year), YearType.ABSOLUTE)
    for japanese_relative_year in prefixes["date_relative_year"]:
        if year == japanese_relative_year:
            return Year(parse_relative_year_value(year), YearType.RELATIVE)
    return Year(dirty_mixed_number_to_value(year), YearType.ABSOLUTE)
