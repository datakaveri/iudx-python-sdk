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
        Request.__init__()
        return

    def get(self, url: str, path_params: Dict, headers: Dict) -> HTTPResponse:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        s = Session()
        reqeust = Request('GET', url, data=path_params, headers=headers)
        prepped = reqeust.prepare()

        resp = s.send(prepped)
        print(resp)
        response = HTTPResponse(resp)
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
