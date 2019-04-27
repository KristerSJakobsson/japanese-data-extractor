import regex

from src.extractor.constants import separators
from src.extractor.models.ExtractedData import ExtractedList
from src.extractor.models.RegexHandler import RegexHandler
from src.utils.conversion_utils import parse_phone_number
from src.utils.io_utils import load_regex

PHONE_NUMBER_REGEX_STRING = load_regex(regex_file_name="postal_code.regexp")
PHONE_NUMBER_REGEX = regex.compile(
    PHONE_NUMBER_REGEX_STRING,
    seperator_phone_number=separators["dash"] + separators["blank"],
    # Seperator: Dash & Blanks
    seperator_space=separators["blank"],  # Seperator: Blanks
    seperator_left_parenthesis=separators["left_parenthesis"],  # Seperator: Left Paranthesis
    seperator_right_parenthesis=separators["right_parenthesis"]  # Seperator: Right Paranthesis
)
PHONE_NUMBER_REGEX_IDENTIFIERS = {
    "phone_number_string": lambda raw_value: raw_value,
    "phone_number_value": parse_phone_number
}


def extract_all_phone_numbers(target_string: str) -> ExtractedList:
    extractor = RegexHandler(compiled_regex=PHONE_NUMBER_REGEX,
                             regex_identifiers=PHONE_NUMBER_REGEX_IDENTIFIERS)
    return extractor.search_string(target_string=target_string)
