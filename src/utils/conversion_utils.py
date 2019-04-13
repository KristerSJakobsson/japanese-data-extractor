from collections import namedtuple
from typing import Optional

from src.extractor.constants import prefixes, special_values
from src.extractor.models.DateValue import Year, Month, Day, DateValueType
from src.extractor.models.PostalCode import PostalCode
from src.extractor.models.TimeDecorator import TimeDecorator
from src.utils.number_conversion_utils import dirty_mixed_number_to_value, clean_mixed_number_to_value
from src.utils.number_conversion_utils import japanese_container_dict, parse_single_char_kanji_as_number

HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000

FULL2HALF = dict((i + 0xFEE0, i) for i in range(0x21, 0x7F))
FULL2HALF[0x3000] = 0x20


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


def parse_time_decorator(decorator_string: str) -> Optional[TimeDecorator]:
    """
    Coverts decorator value to the corresponding enum value.
    :return: An enum representation AM and PM input
    """
    if decorator_string == "":
        return None
    elif decorator_string == "午後":
        return TimeDecorator.PM
    elif decorator_string == "午前":
        return TimeDecorator.AM
    else:
        raise ValueError(f"The decorator could not be parsen: {decorator_string}")


def parse_time_hour(hour_string: str) -> int:
    """
    Coverts and input hour value to the corresponding int.
    :return: A numerical representation fo the input minues
    """
    return clean_mixed_number_to_value(hour_string)


def parse_time_minutes(minutes_string: str) -> int:
    """
    Converts an input minute value to the corresponding int.
    :return: A numerical representation of the input minutes.
    """
    if minutes_string in special_values["time_half_hour"]:
        # Special case for 半
        return 30
    else:
        return clean_mixed_number_to_value(minutes_string)


def parse_postal_code(postal_code: str) -> PostalCode:
    """
    Function used to convert postal code to default model
    :param postal_code: Some postal code, possibly formatted with kanji or full-width numbers
    :return: Correctly formatted postal code nnn-nnnn
    """
    converted_code = ""

    # Assume it's not a japanese number, contains only numbers and seperator
    for char in postal_code:
        if char.isdigit():
            converted_code = converted_code + full_width_string_to_half_width(char)
        elif char in japanese_container_dict["0to9"]:
            converted_code = converted_code + str(parse_single_char_kanji_as_number(char)[0])

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


def parse_year(year: Optional[str]) -> Optional[Year]:
    """
    Function used to contain year (relative or fixed) to a number
    :param year: Either a year or a relative year
    :return: Either a fixed year or a relative year
    """

    if not year:
        return None
    for japanese_year_prefix in prefixes["date_japanese_year"]:
        if year.startswith(japanese_year_prefix):
            return Year(parse_japanese_year_value(year), DateValueType.ABSOLUTE)
    for japanese_relative_year in prefixes["date_relative_year"]:
        if year == japanese_relative_year:
            return Year(parse_relative_year_value(year), DateValueType.RELATIVE)
    return Year(dirty_mixed_number_to_value(year), DateValueType.ABSOLUTE)


def parse_relative_month_value(relative_month: str) -> int:
    """
    Parses a relative month value such as "前月"
    :param relative_month: The month to parse
    :return: An integer representing the relative value of the year, for example -1
    """
    if relative_month == "前月":
        return -1
    if relative_month == "今月":
        return 0
    if relative_month == "来月":
        return 1
    raise ValueError(f"Could not parse the input as a relative month: {relative_month}")


def parse_month(month: Optional[str]) -> Optional[Month]:
    """
    Function used to contain month (relative or fixed) to a number
    :param month: Either a month or a relative month
    :return: Either a fixed month or a relative month
    """

    if not month:
        return None
    for japanese_relative_month in prefixes["date_relative_month"]:
        if month == japanese_relative_month:
            return Month(parse_relative_month_value(month), DateValueType.RELATIVE)
    return Month(dirty_mixed_number_to_value(month), DateValueType.ABSOLUTE)


def parse_relative_day_value(relative_day: str) -> int:
    """
    Parses a relative day value such as "昨日"
    :param relative_day: The day to parse
    :return: An integer representing the relative value of the day, for example -1
    """
    if relative_day == "前月":
        return -1
    if relative_day == "今月":
        return 0
    if relative_day == "来月":
        return 1
    raise ValueError(f"Could not parse the input as a relative month: {relative_day}")


def parse_day(day: Optional[str]) -> Optional[Day]:
    """
    Function used to contain month (relative or fixed) to a number
    :param day: Either a day or a relative day
    :return: Either a fixed day or a relative day
    """

    if not day:
        return None
    for japanese_relative_month in prefixes["date_relative_month"]:
        if day == japanese_relative_month:
            return Day(parse_relative_day_value(day), DateValueType.RELATIVE)
    return Day(dirty_mixed_number_to_value(day), DateValueType.ABSOLUTE)
