"""Module doc string. Leave empty for now.

HTTPEntity.py
"""

from requests import Request, Session
from typing import TypeVar, Generic, Dict


HTTPEntity = TypeVar('T')
HTTPResponse = TypeVar('T')


class HTTPEntity(Request):
    """Class documentation. Be a little descriptive here.

    Args:
        argument (argument-type): argument-description
    Returns:
        returned-varaible (returned-varaible-type): return-variable-description
    """

    def __init__(self: HTTPEntity, cert: Dict):
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        Request.__init__(self)
        return

    def get(self, url: str, path_params: Dict, headers: Dict) -> HTTPResponse:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        s = Session()
        request = Request('GET', url, data=path_params, headers=headers)
        prepared_req = request.prepare()

        response: HTTPResponse = s.send(prepared_req)
        return response

    def delete(self, url: str, path_params: Dict, 
               headers: Dict) -> HTTPResponse:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        response = HTTPResponse()
        return response

    def post(self, url: str, body: Dict, headers: Dict) -> HTTPResponse:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        response = HTTPResponse()
        return response

    def update(self, url: str, body: Dict, headers: Dict) -> HTTPResponse:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        response = HTTPResponse()
        return response
