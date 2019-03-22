# Tests /src/execution/analyse

import unittest
import jsonpickle
from os.path import join

from src.utils.io_utils import is_file
from src.downloader.wikipedia.wikipedia_downloader import get_wikipedia_data_for_output
from definitions import TEST_DATA_PATH


class TestDownloadWikipediaPages(unittest.TestCase):

    def test_download_and_store_wikipedia_pages(self):
        pages = ["リーマン・ショック", "平均寿命"]
        downloaded_pages = get_wikipedia_data_for_output(pages)

        stringified_pages = list()
        for index, value in enumerate(downloaded_pages):
            self.assertEqual(pages[index], value.title)
            self.assertIsNot(value.title, "")
            self.assertIsNot(value.data, "")
            stringified_pages.append(value)

        output_json_file_name = join(TEST_DATA_PATH, 'test_pages.json')
        json_object = jsonpickle.encode(stringified_pages)
        with open(output_json_file_name, 'w') as my_file:
            my_file.write(json_object)

        self.assertTrue(is_file(output_json_file_name))