import regex

from src.extractor.constants import separators, prefixes
from src.extractor.models.ExtractedData import ExtractedList
from src.extractor.models.RegexHandler import RegexHandler
from src.utils.conversion_utils import parse_postal_code
from src.utils.io_utils import load_regex
from src.utils.number_conversion_utils import japanese_container_dict

POSTAL_CODE_REGEX_STRING = load_regex(regex_file_name="postal_code.regexp")
POSTAL_CODE_REGEX = regex.compile(
    POSTAL_CODE_REGEX_STRING,
    seperator_postal_code=separators["postal_code_numbers"],
    prefix_postal_code=prefixes["postal_code"],
    seperator_space=separators["blank"],
    kanji_0to9=japanese_container_dict["0to9"],
    separator_postal_code_kanji=separators["postal_code_kanji"]
)
POSTAL_CODE_REGEX_IDENTIFIERS = {
    "postal_code_string": lambda raw_value: raw_value,
    "postal_code_value": parse_postal_code
}


def extract_all_postal_codes(target_string: str) -> ExtractedList:
    extractor = RegexHandler(compiled_regex=POSTAL_CODE_REGEX,
                             regex_identifiers=POSTAL_CODE_REGEX_IDENTIFIERS)
    return extractor.search_string(target_string=target_string)

