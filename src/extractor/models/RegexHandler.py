from typing import Tuple, List, Pattern, Dict, Callable
from src.extractor.models.ExtractedData import ExtractedList


class RegexHandler:
    """
    This object contains precompiled regexes, search results and other related data.
    This contains:
    - A precompiled regular expression
    - A dictionary of mappings with conversions from the various fields in the regular expression
    """

    def __init__(self, compiled_regex: Pattern,
                 regex_identifiers: Dict[str, Callable[[Tuple[str, str]], ExtractedList]]) -> None:
        if compiled_regex is None or regex_identifiers is None:
            raise ValueError("Tried to save an empty regex or identifier list to a RegexHandler!")
        self._regex_identifiers = regex_identifiers  # A list of identifiers in the regex
        self._compiled_regex = compiled_regex
        self._result_stored_list = []  # List of match objects
        self._loaded_string = ""

    def search_string(self, target_string: str, post_process: Callable = None) -> ExtractedList:
        """
        Ensures that all results up to the input order is stored in the object.
        :param target_string String to extract data from
        """
        extracted_data = []
        for match in self._compiled_regex.finditer(target_string):
            capture_groups = match.groupdict()
            regex_span = match.span()
            capture_data = {}
            for key, value in capture_groups.items():
                capture_data[key] = self._regex_identifiers[key](value)
            extracted_data.append((regex_span, capture_data))

        if post_process:
            extracted_data = [post_process(data) for data in extracted_data]

        return extracted_data
