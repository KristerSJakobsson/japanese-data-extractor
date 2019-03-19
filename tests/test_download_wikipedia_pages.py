# Tests /src/execution/analyse

import unittest
import json
from os.path import join

from src.utils.io_utils import is_file
from src.downloader.wikipedia.wikipedia_downloader import download_wikipedia_pages
from definitions import TEST_DATA_PATH


class TestDownloadWikipediaPages(unittest.TestCase):

    def test_download_and_store_wikipedia_pages(self):
        pages = ["リーマン・ショック", "平均寿命"]
        downloaded_pages = download_wikipedia_pages(pages)

        stringified_pages = dict()
        for index, value in enumerate(downloaded_pages):
            self.assertEqual(pages[index], value.title)
            self.assertIsNot(value.title, "")
            self.assertIsNot(value.text, "")
            stringified_pages[value.title] = value.text

        output_json_file_name = join(TEST_DATA_PATH, 'test_pages.json')
        with open(output_json_file_name, 'w') as file_stream:
            json.dump(stringified_pages, file_stream)

        self.assertTrue(is_file(output_json_file_name))