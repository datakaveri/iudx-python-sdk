"""Module doc string. Leave empty for now.

HTTPEntity.py
"""

from requests import Request, Session
from typing import TypeVar, Generic, Dict


HTTPEntity = TypeVar('T')
HTTPResponse = TypeVar('T')


class HTTPEntity(Request):
    """Abstract class for Requests. Helps to create a modular interface
       for the API Request in Python.
    """

    def __init__(self: HTTPEntity, cert: Dict=None):
        """HTTPEntity base class constructor
        Args:
            cert (Dict): certificate for authentication.
        """
        Request.__init__(self)
        return

    def get(self, url: str, path_params: Dict, headers: Dict) -> HTTPResponse:
        """Method to create a 'GET' API request and returns response.

        Args:
            url (String): Base URL for the API Request.
            path_params (Dict): Parameters passed with the API Request.
            headers (Dict): Headers passed with the API Request.
        Returns:
            response (HTTPResponse): HTTP Response after the API Request.
        """
        s = Session()
        request = Request('GET', url, params=path_params, headers=headers)
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
