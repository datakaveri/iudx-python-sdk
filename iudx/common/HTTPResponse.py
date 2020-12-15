"""Module doc string. Leave empty for now.

HTTPEntity.py
"""
from requests import Request
from requests import Response
from typing import TypeVar, Generic, Dict


HTTPResponse = TypeVar('T')

class HTTPResponse(Response):
    """Class documentation. Be a little descriptive here.

    Args:
        argument (argument-type): argument-description
    Returns:
        returned-varaible (returned-varaible-type): return-variable-description
    """

    def __init__(self: HTTPResponse):
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        self._response = Response.__init__()
        return

    def json(self) -> Dict :
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self._response.json()

    def status_code(self) -> int :
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self._response.status_code
