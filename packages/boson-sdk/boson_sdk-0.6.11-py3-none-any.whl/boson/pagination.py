from typing import Tuple


class Pagination:
    """Pagination class to manage pagination tokens, page/page_size and links

    Args:
        pagination (dict): pagination dictionary passed to the search func
        page_size (int): page size passed in as the 'limit` parameter of the search func
    """

    def __init__(self, pagination: dict, page_size: int):
        self.page_size = page_size
        self.resource_index = 0
        self.offset = 0
        self.link = None
        self.token = None
        self._parse_pagination(pagination)
        self._next_called = False

    def _parse_pagination(self, pagination: dict):
        if "page" in pagination and "page_size" in pagination:
            self.page_size = pagination["page_size"]
            self.resource_index = 0
            self.offset = pagination.get("page", 0) * self.page_size
        elif "token" in pagination:
            self.parse_token(pagination["token"])
        elif "link" in pagination:
            self.link = pagination["link"]

    def get_current_token(self) -> str:
        """returns the current token

        Returns:
            str: the current token
        """
        if self.token:
            return self.token
        return f"{self.offset}-{self.page_size}-{self.resource_index}"

    def get_current(self) -> Tuple[int, int, int]:
        """returns the current offset, page size and resource index"""
        return self.offset, self.page_size, self.resource_index

    def parse_token(self, token: str):
        """parses the token into offset, page size and resource index or leaves it as is

        If the token is a hyphen-separated string, it is parsed into offset, page size and resource index.
        Otherwise, it is left as is.

        Args:
            token (str): the token to parse
        """
        if not token:
            return 0, self.limit, 0
        try:
            offset, page_size, resource_index = token.split("-")
        except Exception:
            self.token = token
            return

        self.resource_index = int(resource_index)
        self.offset = int(offset)
        self.limit = int(page_size)

    def get_next_token(self, offset: int, resource_index: int = 0) -> str:
        """returns the next token with an updated offset and resource index

        IMPORTANT: this method alters the current offset and resource index, so it should be called
        once and only once before returning from the search function
        """
        if self._next_called:
            raise ValueError("get_next_token should be called only once per request")

        self.resource_index = resource_index
        self.offset = offset
        self._next_called = True
        return self.get_current_token()
