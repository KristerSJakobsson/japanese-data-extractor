import regex

from src.extractor.models.RegexHandler import RegexHandler
from src.extractor.models.ExtractedData import ExtractedData
from src.utils.io_utils import load_regex

from src.extractor.constants import separators, prefixes
from src.utils.number_conversion_utils import japanese_container_dict
from src.utils.conversion_utils import parse_postal_code

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


def extract_postal_code(target_string: str) -> ExtractedData:
    extractor = RegexHandler(compiled_regex=POSTAL_CODE_REGEX,
                             regex_identifiers=POSTAL_CODE_REGEX_IDENTIFIERS)
    return extractor.search_string(target_string=target_string)
