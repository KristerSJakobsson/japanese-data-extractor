import regex

from src.extractor.models.RegexHandler import RegexHandler
from src.extractor.models.ExtractedData import ExtractedList
from src.utils.io_utils import load_regex

from src.extractor.constants import separators, prefixes, suffixes
from src.utils.number_conversion_utils import japanese_container_dict
from src.utils.conversion_utils import parse_postal_code, parse_year, parse_month, parse_day

# POSTAL CODE

POSTAL_CODE_REGEX_STRING = load_regex(regex_file_name="postal_code.regexp")
POSTAL_CODE_REGEX = regex.compile(
    POSTAL_CODE_REGEX_STRING,
    seperator_postal_code=separators["dash"] + separators["blank"],
    prefix_postal_code=prefixes["postal_code"],
    seperator_space=separators["blank"],
    kanji_0to9=japanese_container_dict["0to9"]
)
POSTAL_CODE_REGEX_IDENTIFIERS = {
    "postal_code_string": lambda raw_value: raw_value,
    "postal_code_value": lambda raw_value: parse_postal_code(postal_code=raw_value)
}


def extract_all_postal_codes(target_string: str) -> ExtractedList:
    extractor = RegexHandler(compiled_regex=POSTAL_CODE_REGEX,
                             regex_identifiers=POSTAL_CODE_REGEX_IDENTIFIERS)
    return extractor.search_string(target_string=target_string)


# DATE

DATE_REGEX_STRING = load_regex(regex_file_name="date.regexp")
DATE_REGEX = regex.compile(
    DATE_REGEX_STRING,
    prefix_relative_year=prefixes["date_relative_year"],
    prefix_relative_month=prefixes["date_relative_month"],
    prefix_japanese_year_names=prefixes["date_japanese_year"],
    suffix_day=suffixes["date_japanese_day"],
    suffix_day_like=suffixes["date_japanese_day_exceptions"],
    suffix_month=suffixes["date_japanese_month"],
    suffix_year=suffixes["date_japanese_year"],
    separator_year_month_day=separators["dash"] + separators["blank"] + separators["slash"],
    seperator_space=separators["blank"],
    kanji_0to1=japanese_container_dict["0to1"],
    kanji_0to2=japanese_container_dict["0to2"],
    kanji_0to9=japanese_container_dict["0to9"],
    kanji_0to1000=japanese_container_dict["0to1000"],
    kanji_1=japanese_container_dict["1"],
    kanji_1to2=japanese_container_dict["1to2"],
    kanji_1to9=japanese_container_dict["1to9"],
    kanji_2=japanese_container_dict["2"],
    kanji_2to9=japanese_container_dict["2to9"],
    kanji_3=japanese_container_dict["3"],
    kanji_10=japanese_container_dict["10"]
)

DATE_REGEX_IDENTIFIERS = {
    "date_string": lambda raw_value: raw_value,
    "date_year": lambda raw_value: parse_year(year=raw_value),
    "date_month": lambda raw_value: parse_month(month=raw_value),
    "date_day": lambda raw_value: parse_day(day=raw_value)
}


def extract_all_dates(target_string: str) -> ExtractedList:
    extractor = RegexHandler(compiled_regex=DATE_REGEX,
                             regex_identifiers=DATE_REGEX_IDENTIFIERS)
    return extractor.search_string(target_string=target_string)
