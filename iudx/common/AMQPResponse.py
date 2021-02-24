"""Module doc string. Leave empty for now.

AMQPEntity.py
"""
from requests import Response
from typing import TypeVar, Dict


AMQPResponse = TypeVar('T')


class AMQPResponse():
    """Abstract class for Response. Helps to create a modular interface
       for the API Response in Python.
    """

    def __init__(self: AMQPResponse):
        """AMQPResponse base class constructor
        """
        self._response = None
        return

    def get_json(self) -> Dict:
        """Method to return the json object for the response body.

        Returns:
            result_json (Dict): Returns json data.
        """
        result_json = self._response.json()
        return result_json

    def get_status_code(self) -> int:
        """Method to return the status code for the response.

        Returns:
            status (Integer): Returns numerical status code for the Response.
        """
        status = self._response.status_code
        return status
