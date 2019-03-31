from typing import Tuple, List, Pattern, Dict, Callable
from src.extractor.models.ExtractedData import ExtractedData

ConverterMapping = Tuple[str, object]  # Maps how an item should be converted


class RegexHandler:
    """
    This object contains precompiled regexes, search results and other related data.
    This contains:
    - A precompiled regular expression
    - A dictionary of mappings with conversions from the various fields in the regular expression
    """

    def __init__(self, compiled_regex: Pattern,
                 regex_identifiers: Dict[str, Callable[[Tuple[str, str]], ExtractedData]]) -> None:
        if compiled_regex is None or regex_identifiers is None:
            raise ValueError("Tried to save an empty regex or identifier list to a RegexHandler!")
        self._regex_identifiers = regex_identifiers  # A list of identifiers in the regex
        self._compiled_regex = compiled_regex
        self._result_stored_list = []  # List of match objects
        self._loaded_string = ""

    def search_string(self, target_string: str) -> ExtractedData:
        """
        Ensures that all results up to the input order is stored in the object.
        :param target_string String to extract data from
        """
        regex_matches = self._compiled_regex.findall(target_string)

        extracted_data = {match[0]: self._regex_identifiers[match[1]]() for match in regex_matches}

        return extracted_data

    @property
    def regex_identifier(self) -> List[str]:
        """
        Returns a list of identifiers for this regex.
        :rtype: List[str]
        """
        return list(self._regex_identifiers.keys())
