"""Module doc string. Leave empty for now.

ResourceResult.py
"""
from typing import TypeVar, Generic, Any, List, Dict

ResourceResult = TypeVar('T')


class ResourceResult():
    """Abstract class for Resource Result. Helps to create a modular
       interface for the API response results.
    """

    def __init__(self: ResourceResult):
        """ResourceResult base class constructor
        """
        self.results: List[Dict] = ""
        self.type: int = 0
        self.title: str = ""
        return
