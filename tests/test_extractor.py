# Tests /src/execution/analyse

import unittest
import jsonpickle

from typing import List
from os.path import join

from definitions import TEST_DATA_PATH
from src.downloader.models.DownloadedData import DownloadedData


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
