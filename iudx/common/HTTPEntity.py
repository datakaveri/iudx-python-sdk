"""Module doc string. Leave empty for now.

HTTPEntity.py
"""

from requests import Request, Session
from typing import TypeVar, Dict


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

    def get(self, url: str, headers: Dict) -> HTTPResponse:
        """Method to create a 'GET' API request and returns response.

        Args:
            url (String): Base URL for the API Request.
            path_params (Dict): Parameters passed with the API Request.
            headers (Dict): Headers passed with the API Request.
        Returns:
            response (HTTPResponse): HTTP Response after the API Request.
        """
        s = Session()
        request = Request('GET',
                          url,
                          headers=headers)
        prepared_req = request.prepare()

        response: HTTPResponse = s.send(prepared_req)
        return response

    def delete(self, url: str, headers: Dict) -> HTTPResponse:
        """Method to create a 'DELETE' API request and returns response.

        Args:
            url (String): Base URL for the API Request.
            path_params (Dict): Parameters passed with the API Request.
            headers (Dict): Headers passed with the API Request.
        Returns:
            response (HTTPResponse): HTTP Response after the API Request.
        """
        s = Session()
        request = Request('DELETE',
                          url,
                          headers=headers)
        prepared_req = request.prepare()

        response: HTTPResponse = s.send(prepared_req)
        return response

    def post(self, url: str, body: Dict, headers: Dict) -> HTTPResponse:
        """Method to create a 'POST' API request and returns response.

        Args:
            url (String): Base URL for the API Request.
            body (Dict): Data for the body passed with the API Request.
            headers (Dict): Headers passed with the API Request.
        Returns:
            response (HTTPResponse): HTTP Response after the API Request.
        """
        s = Session()
        request = Request('POST', url, data=body, headers=headers)
        prepared_req = request.prepare()

        response: HTTPResponse = s.send(prepared_req)
        return response

    def update(self, url: str, body: Dict, headers: Dict) -> HTTPResponse:
        """Method to create a 'PUT' API request and returns response.

        Args:
            url (String): Base URL for the API Request.
            body (Dict): Data for the body passed with the API Request.
            headers (Dict): Headers passed with the API Request.
        Returns:
            response (HTTPResponse): HTTP Response after the API Request.
        """
        s = Session()
        request = Request('PUT', url, data=body, headers=headers)
        prepared_req = request.prepare()

        response: HTTPResponse = s.send(prepared_req)
        return response
