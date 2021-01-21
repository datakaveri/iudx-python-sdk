"""Module doc string. Leave empty for now.

Entities.py
"""
from typing import TypeVar, Generic, Any, List, Dict
from iudx.entity.Entity import Entity

Entities = TypeVar('T')


class Entities():
    """Abstract class for Entities. Helps to create a modular interface
       for the list of entities.
    """

    def __init__(self: Entities):
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        self._entities: List[Entity] = []
        return
