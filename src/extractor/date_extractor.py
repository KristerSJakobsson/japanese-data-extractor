from typing import Tuple, Optional

import regex

from src.extractor.constants import separators, prefixes, suffixes
from src.extractor.models.ComplexDate import ComplexDate
from src.extractor.models.DateValue import Year, Month, Day
from src.extractor.models.ExtractedData import ExtractedList, ExtractedDataPosition, ExtractedData
from src.extractor.models.RegexHandler import RegexHandler
from src.utils.conversion_utils import parse_year, parse_month, parse_day
from src.utils.io_utils import load_regex
from src.utils.number_conversion_utils import japanese_container_dict

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
    "date_year": parse_year,
    "date_month": parse_month,
    "date_day": parse_day
}


def date_post_processing(extracted_data: Tuple[ExtractedDataPosition, ExtractedData]):
    """
    Adds the aggregated complex date to the list of extracted values
    :param extracted_data: The extracted data (tuple with position of match and the extracted data)
    :return: Same tuple as extracted_data but with the additional date field added to extracted data
    """
    extracted_data_dictionary = extracted_data[1]

    year: Optional[Year] = extracted_data_dictionary["date_year"]
    month: Optional[Month] = extracted_data_dictionary["date_month"]
    day: Optional[Day] = extracted_data_dictionary["date_day"]

    extracted_data_dictionary["date"] = ComplexDate(year=year, month=month, day=day)

    return extracted_data[0], extracted_data_dictionary


def extract_all_dates(target_string: str) -> ExtractedList:
    extractor = RegexHandler(compiled_regex=DATE_REGEX,
                             regex_identifiers=DATE_REGEX_IDENTIFIERS)
    return extractor.search_string(target_string=target_string, post_process=date_post_processing)
