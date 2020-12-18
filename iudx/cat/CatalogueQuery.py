"""Module doc string. Leave empty for now.

CatalogueQuery.py
"""

from typing import TypeVar, Generic, Any, List, Dict

CatalogueQuery = TypeVar('T')


class CatalogueQuery():
    """Class documentation. Be a little descriptive here.

    Args:
        argument (argument-type): argument-description
    Returns:
        returned-varaible (returned-varaible-type): return-variable-description
    """

    def __init__(self: CatalogueQuery):
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        self._groproperty: str = ""
        self._geometry: str = ""
        self._georel: str = ""
        self._coordinates: List[Any] = []
        self._text_query: str = ""
        self._key: List[str] = []
        self._value: List[List[str]] = []
        self._filters: List[str] = []
        return

    def geo(self, geoproperty: str, geometry: str, georel: str,
                coordinates: List[Any]) -> CatalogueQuery: 
        """Pydoc heading.

        Args: 
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def property(self, key: str, value: List[str]) -> CatalogueQuery:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def text(self, text_query: str) -> CatalogueQuery:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def add_filter(self, filters: List[str]) -> CatalogueQuery:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self
