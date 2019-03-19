# Tests /src/execution/analyse

import unittest
import json

from typing import Dict, Optional
from os.path import join

from definitions import TEST_DATA_PATH


class TestExtract(unittest.TestCase):

    @staticmethod
    def _load_test_data() -> Dict[str, str]:
        input_json_file_name = join(TEST_DATA_PATH, 'test_pages.json')
        with open(input_json_file_name, 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def _dummy_extract_data(data: str) -> str:
        # TODO: Implement this!
        return data

    def test_load_inexistent_file(self):
        test_data = TestExtract._load_test_data()
        test_result = dict()
        for key in test_data.keys():
            test_result[key] = TestExtract._dummy_extract_data(test_data[key])


