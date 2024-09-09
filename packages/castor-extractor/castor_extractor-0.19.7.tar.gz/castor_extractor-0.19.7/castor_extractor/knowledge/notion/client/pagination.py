from typing import Optional

from ....utils import PaginationModel


class NotionPagination(PaginationModel):
    """Class to handle paginated results"""

    results: list
    next_cursor: Optional[str]
    has_more: bool

    def is_last(self) -> bool:
        return not self.has_more

    def next_page_payload(self) -> dict:
        return {"start_cursor": self.next_cursor}

    def page_results(self) -> list:
        return self.results
