"""Module doc string. Leave empty for now.

CatalogueResult.py
"""
from typing import TypeVar, Generic, Any, List, Dict

CatalogueResult = TypeVar('T')


class CatalogueResult():
    """Abstract class for Resource Result. Helps to create a modular
       interface for the API response results.
    """

    def __init__(self: CatalogueResult):
        """CatalogueResult base class constructor
        """
        self._page_size: str = 1000
        self.documents: List[Dict] = ""
        self.total_hits: int = 0
        self.total_pages: int = 0
        self.current_page: int = 0
        self.is_valid: bool = False
        self.status: str = ""
        return

    def next_page(self) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def goto_page(self, pagenume: int) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def all_pages(self) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self
