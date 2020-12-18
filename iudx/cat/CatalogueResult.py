"""Module doc string. Leave empty for now.

CatalogueResult.py
"""
from typing import TypeVar, Generic, Any, List, Dict

CatalogueResult = TypeVar('T')


class CatalogueResult():
    """Class documentation. Be a little descriptive here.

    Args:
        argument (argument-type): argument-description
    Returns:
        returned-varaible (returned-varaible-type): return-variable-description
    """

    def __init__(self: CatalogueResult):
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        self._page_size: str = 1000
        self.documents: List[Dict] = ""
        self.total_hits: int = 0
        self.total_pages: int = 0
        self.current_page: int = 0
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
