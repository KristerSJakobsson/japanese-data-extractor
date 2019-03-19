#!/usr/bin/python

import sys
from typing import List, Any, Tuple
from getopt import getopt, GetoptError

from src.utils.io_utils import create_directory_if_not_exists


def _parse_parameters_and_arguments(argv: List[str]) -> Tuple[List[str], str]:
    try:
        extracted_options, extracted_arguments = getopt(argv, "hp:", ["help", "page="])
    except GetoptError as err:
        print(err)
        _display_usage_text()
        sys.exit(2)

    target_pages = _parse_options_for_extraction(extracted_options)
    output_path = _parse_arguments_for_extraction(extracted_arguments)

    return target_pages, output_path


def _parse_options_for_extraction(options: List[Any]) -> List[str]:
    """
    Takes option for the executed script
    :param options: A list of options specified at execution
    :return: A ClassifierDetails object representing the options specified (or default if not specified)
    """

    target_pages = list()

    try:
        for option, value in options:
            if option in ("-h", "--help"):
                _display_usage_text()
                sys.exit(2)
            elif option in ("-p", "--pages"):
                target_pages = _validate_page_input(value)
            else:
                raise RuntimeError("Invalid option " + option)
    except Exception as err:
        print(err)
        _display_usage_text()
        sys.exit(2)

    return target_pages


def _parse_arguments_for_extraction(argument: str) -> str:
    """
    Parse the arguments for the extractor
    :param argument: A path to the folder where the results should be output
    """


def _validate_page_input(page_input: str) -> List[str]:
    """
    Validate the page input value
    :param page_input: Pages to parse
    """
    if not page_input:
        raise ValueError(
            "Invalid input for pages, please input one or more pages seperated by ;;")

    return page_input.split(";;")


def _validate_path_output(path: str) -> str:
    """
    Validate the path where the results should beo utput
    :param path: A valid path
    """
    create_directory_if_not_exists(path)
    return path


def _display_usage_text() -> None:
    """
    Shows the explanation for parameters and arguments
    """
    print("""Specify a path to either the path to a file with text to process (.txt) or 
    a path with several such files.""")


if __name__ == "__main__":
    pages, path = _parse_parameters_and_arguments(sys.argv[1:])
