class PageNotFoundError(Exception):
    def __init__(self, page_name: str, page_source: str):
        self.page_name = page_name
        self.page_source = page_source

        super().__init__('page_name: {}, page_source: {}'.format(page_name, page_source))

    def __reduce__(self):
        return self.__class__, (self.page_name, self.page_source)
