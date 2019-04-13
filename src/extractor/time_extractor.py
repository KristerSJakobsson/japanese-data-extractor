from datetime import time
from typing import Optional, Tuple

import regex

from src.extractor.constants import separators, prefixes, suffixes, special_values
from src.extractor.models.ExtractedData import ExtractedList, ExtractedDataPosition, ExtractedData
from src.extractor.models.RegexHandler import RegexHandler
from src.extractor.models.TimeDecorator import TimeDecorator
from src.utils.conversion_utils import parse_time_minutes, parse_time_hour, parse_time_decorator
from src.utils.io_utils import load_regex
from src.utils.number_conversion_utils import japanese_container_dict

TIME_REGEX_STRING = load_regex(regex_file_name="time.regexp")
TIME_REGEX = regex.compile(
    TIME_REGEX_STRING,
    prefix_hour_decorator=prefixes["time_hour"],
    suffix_hour=suffixes["time_hour"],
    suffix_minute=suffixes["time_minute"],
    special_value_half_hour=special_values["time_half_hour"],
    separator_hour_minute=separators["colon"],
    suffix_hour_like=suffixes["time_hour_like"],
    kanji_0=japanese_container_dict["0"],
    kanji_0to1=japanese_container_dict["0to1"],
    kanji_0to4=japanese_container_dict["0to4"],
    kanji_0to5=japanese_container_dict["0to5"],
    kanji_0to9=japanese_container_dict["0to9"],
    kanji_0to10=japanese_container_dict["0to10"],
    kanji_1to4=japanese_container_dict["1to4"],
    kanji_1to5=japanese_container_dict["1to5"],
    kanji_1to9=japanese_container_dict["1to9"],
    kanji_2=japanese_container_dict["2"],
    kanji_6=japanese_container_dict["6"],
    kanji_10=japanese_container_dict["10"]
)
TIME_REGEX_IDENTIFIERS = {
    "time_string": lambda raw_value: raw_value,
    "time_decorator": parse_time_decorator,
    "time_hour": parse_time_hour,
    "time_minute": parse_time_minutes,
}


def time_post_processing(extracted_data: Tuple[ExtractedDataPosition, ExtractedData]):
    """
    Adds the aggregated complex date to the list of extracted values
    :param extracted_data: The extracted data (tuple with position of match and the extracted data)
    :return: Same tuple as extracted_data but with the additional date field added to extracted data
    """
    extracted_data_dictionary = extracted_data[1]

    time_decorator: Optional[TimeDecorator] = extracted_data_dictionary["time_decorator"]
    hour: int = extracted_data_dictionary["time_hour"]
    minute: int = extracted_data_dictionary["time_minute"]

    if time_decorator == TimeDecorator.PM:
        hour = hour + 12

    extracted_data_dictionary["time"] = time(hour=hour, minute=minute)

    return extracted_data[0], extracted_data_dictionary


def extract_all_times(target_string: str) -> ExtractedList:
    extractor = RegexHandler(compiled_regex=TIME_REGEX,
                             regex_identifiers=TIME_REGEX_IDENTIFIERS)
    return extractor.search_string(target_string=target_string)
