"""Module doc string. Leave empty for now.

Catalogue.py
"""

from typing import TypeVar, Generic, Any, List, Dict

from iudx.cat import Catalogue

Catalogue = TypeVar("T")
CatalogueResult = TypeVar("T")
CatalogueQuery = TypeVar("T")


class Catalogue():
    """Class documentation. Be a little descriptive here.

    Args:
        argument (argument-type): argument-description
    Returns:
        returned-varaible (returned-varaible-type): return-variable-description
    """
    
    def __init__(self, cat_url: str=None, token: str=None,
                    headers: Dict[str, str]=None):
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        self.url: str = ""
        self.token: str = ""
        self.headers: Dict[str, str] = ""
        return

    def status(self) -> bool:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def search(self, query: CatalogueQuery) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def count(self, query: CatalogueQuery) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def list_entity(self, entity_type: str) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def get_related_entity(self, iid: str, rel: str) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def rel_search(self, query: CatalogueQuery) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def get_item(self, iid: str) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def create(self, item: Dict[str, Any]) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def update(self, item: Dict[str, Any]) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def delete(self, iid: str) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def validate(self, item: Dict[str, Any]) -> bool:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return False

    def update_token(self, token: str) -> None:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return None
