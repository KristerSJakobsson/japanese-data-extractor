# Tests /src/execution/analyse

import unittest
import jsonpickle
import regex

from typing import List
from os.path import join

from definitions import TEST_DATA_PATH
from src.downloader.models.DownloadedData import DownloadedData
from src.extractor.models.RegexHandler_old import RegexHandler
from src.extractor.postal_code_extractor import extract_postal_code
from src.extractor.models.PostalCode import PostalCode


class TestExtract(unittest.TestCase):

    @staticmethod
    def _load_test_data() -> List[DownloadedData]:
        input_json_file_name = join(TEST_DATA_PATH, 'test_pages.json')
        with open(input_json_file_name, 'r') as my_file:
            raw_text = my_file.read()
        return jsonpickle.decode(raw_text)

    @staticmethod
    def _dummy_extract_data(data: str) -> str:
        # TODO: Implement this!
        return data

    def test_load_inexistent_file(self):
        test_data = TestExtract._load_test_data()
        test_result = dict()
        for item in test_data:
            test_result[item.title] = TestExtract._dummy_extract_data(item.data)

    def test_extract_postal_code(self):
        string_containing_postal_code = "今の郵便コードが「012-2321」です。"
        extracted_data = extract_postal_code(target_string=string_containing_postal_code)

        expected_extraction = {
            "postal_code_string": "012-2321",
            "postal_code_value": PostalCode("0122321")
        }

        self.assertEqual(extracted_data, expected_extraction,
                         f"Result {extracted_data} is not the same as expectation {expected_extraction}")
