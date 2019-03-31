from typing import Tuple, List, Pattern, TypeVar, Optional, Dict, Callable

ConverterMapping = Tuple[str, object]  # Maps how an item should be converted
ExtractedData = TypeVar('T', int, str)


class RegexHandler:
    """
    This object contains precompiled regexes, search results and other related data.
    This contains:
    - A precompiled regular expression
    - A dictionary of mappings with conversions from the various fields in the regular expression
    """

    def __init__(self, compiled_regex: Pattern,
                 regex_identifiers: Dict[str, Callable[[object], ExtractedData]]) -> None:
        if compiled_regex is None or regex_identifiers is None:
            raise ValueError("Tried to save an empty regex or identifier list to a RegexHandler!")
        self._regex_identifiers = regex_identifiers  # A list of identifiers in the regex
        self._compiled_regex = compiled_regex
        self._result_stored_list = []  # List of match objects
        self._loaded_string = ""

    def load_string(self, target_string: str) -> None:
        self._result_stored_list = []
        self._loaded_string = target_string

    def search_string(self, result_in_order: int) -> Optional[str]:
        """
        Ensures that all results up to the input order is stored in the object.
        :param result_in_order
        """
        # Note that if an search does not match, it will return None
        if len(self._result_stored_list) >= result_in_order:
            # Result should already be stored! Just return it.
            return self._result_stored_list[result_in_order - 1]
        else:
            # We need to append results to the end of self._result_stored_list
            if len(self._result_stored_list) == 0:
                # Empty list, meaning we just search and append!
                search_start_position = 0
            elif not self._result_stored_list[-1]:
                # Note that if the last item in the list is None (return false),
                # then the most recent search did not find any value,
                # and thus searching again will yield the same result => No need to search again!
                pass
            else:
                # Find the start position from the last item in the list, being the end of the first captured group.
                # Note: This is by design, our Regex always captures the fulls string as the first group!
                search_start_position = self._result_stored_list[-1].end(0)

            # Based on the start position, we need to find and append values up to the input order
            for order in range(len(self._result_stored_list), result_in_order):
                # If we ever get None as the last value, we don't need to search any further!
                if len(self._result_stored_list) == 0 or self._result_stored_list[-1]:
                    self._result_stored_list.append(
                        self._compiled_regex.search(self._loaded_string, search_start_position))
                    # Update start position at end of last found value
                    if self._result_stored_list[-1]:
                        search_start_position = self._result_stored_list[-1].end(0)
                else:
                    self._result_stored_list.append(None)

    def clear_string(self) -> None:
        """
        Removes result and string from object.
        :rtype: None
        """
        self._result_stored_list = []
        self._loaded_string = ""

    def regex_results(self, index: int, identifier: str, process_data: bool) -> ExtractedData:
        """
        List of identifiers for this regex, in case of no match it returns an empty string.
        :rtype: ExtractedData
        """
        if not self._result_stored_list[index]:
            # The result stored for the index is None, meaning no match!
            return ""

        # First of all, the input identifier must be in the list of converter mappings
        for converter_mapping in self._regex_identifiers:
            if converter_mapping[0] == identifier:
                # Good! We found a converter function and call it with the corresponding.
                if process_data:
                    return converter_mapping[1](self._result_stored_list[index][identifier])
                else:  # Ignore converter!
                    return self._result_stored_list[index][identifier]
        else:
            # For-loop didn't return, no item with the specified identifier exists!
            raise ValueError(f"Invalid identifier input: {identifier}")

    @property
    def regex_identifier(self) -> List[str]:
        """
        Returns a list of identifiers for this regex.
        :rtype: List[str]
        """
        return [x[0] for x in self._regex_identifiers]

    @property
    def loaded_string(self):
        """
        Currently loaded string.
        :rtype: str
        """
        return self._loaded_string


class TagHandler:
    """
    This object handles data related to tags, such as precompiled regex etc.
    """

    def __init__(self, tag: str, tag_data: Pattern, compiled_regex: RegexHandler) -> None:
        self.tag_string = tag  # The original string used with the regex
        self.tag_type = tag_data['type']  # The type or regex tag, either cat, tag or word
        self.tag_identifier = tag_data['identifier']  # The type specified, either a kind of tag, category name or word
        self.tag_number = int(tag_data['number']) if tag_data[
                                                         'number'] != '' else -1  # Optional, sets which tag in order it is if several
        self.compiled_regex = compiled_regex  # A compiled regex

    def load_string(self, target_string: str) -> bool:
        if self.compiled_regex.loaded_string == "":
            self.compiled_regex.load_string(target_string)
            return True
        elif target_string == self.compiled_regex.loaded_string:
            return True
        else:
            return False

    def clear_string(self) -> None:
        self.compiled_regex.clear_string()

    def extract_data(self, identifier: str, process_data: bool) -> ExtractedData:
        """
        :type identifier: str
        :type process_data: bool
        """
        self.compiled_regex.search_string(self.tag_number)
        return self.compiled_regex.regex_results(self.tag_number - 1, identifier, process_data)

    @property
    def regex_identifier(self) -> List[str]:
        """Returns a list of identifiers for this regex."""
        return self.compiled_regex.regex_identifier
