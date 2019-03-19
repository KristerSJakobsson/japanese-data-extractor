from typing import List
from wikipediaapi import Wikipedia, WikipediaPage

from src.exceptions.downloader_exceptions import PageNotFoundError

wiki_extractor = Wikipedia(language='ja')


def get_wikipedia_data_for_output(search_page_names: List[str]) -> List[str]:
    pages = download_wikipedia_pages(search_page_names=search_page_names)
    return [page.title + "\n" + page.text for page in pages]


def download_wikipedia_pages(search_page_names: List[str]) -> List[WikipediaPage]:
    pages = list()
    for page_name in search_page_names:
        page = wiki_extractor.page(page_name)
        if not page.exists():
            raise PageNotFoundError(page_name=page_name, page_source="Wikipedia")
        pages.append(page)
    return pages
