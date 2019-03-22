from wikipediaapi import WikipediaPage


class DownloadedData:
    """
    This object represents some data that has been downloaded for use with this tool.
    """

    def __init__(self, title: str, data: str) -> None:
        self.title = title
        self.data = data

    @staticmethod
    def from_wikipedia_page(wikipedia_page: WikipediaPage) -> 'DownloadedData':
        return DownloadedData(wikipedia_page.title, wikipedia_page.text)
