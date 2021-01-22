"""Module doc string. Leave empty for now.

IUDXEntity.py
"""
from typing import TypeVar, Generic, Any, List, Dict

from iudx.cat.Catalogue import Catalogue
from iudx.cat.CatalogueQuery import CatalogueQuery
from iudx.rs.ResourceServer import ResourceServer

from iudx.entity.Entity import Entity
from iudx.entity.Entities import Entities

IUDXEntity = TypeVar('T')


class IUDXEntity():
    """Abstract class for IUDXEntity. Helps to create a modular interface
       for the IUDX Entity.
    """

    def __init__(self):
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        self.catalogue: Catalogue = None

        self._rs: ResourceServer = None
        self._resources: List[Dict] = None
        self._resourceGroups: Dict = None
        return

    def get_resources(self, resourceGroup: str=None) -> List[Dict]:
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self._resources

    def get_resourceGroups(self) -> Dict:
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self._resourceGroups

    def get_entites(self, query: CatalogueQuery=None) -> Entities:
        """Pydoc heading.
        Args:
            argument (argument-type): argument  -description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def get_entity(self, entity_id: str=None) -> Entity:
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self
