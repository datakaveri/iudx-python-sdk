import json

from iudx.common.HTTPEntity import HTTPEntity
from iudx.common.HTTPResponse import HTTPResponse


class Token:
    """
    Provides token functionality for accessing
    the private resources
    """

    def __init__(
            self,
            auth_url: str = "https://authorization.iudx.org.in/auth/v1",
            authorization_token: str = None,
            token_file: str = None,
            client_id: str = None,
            client_secret: str = None,
            headers: dict = None):
        """
        Token class constructor for requesting tokens

        Args:
            auth_url (String): Authorization server url.
            authorization_token (String): Keycloak Issued token.
            token_file (String): Path to Keycloak token file.
            client_id (String): Keycloak Issued clientId.
            client_secret (String): Keycloak Issued clientSecret.
            headers (Dict): Headers passed with the API Request.
        """
        if headers is None:
            headers = {"content-type": "application/json"}

        if authorization_token is not None:
            headers.update({"Authorization": authorization_token})
        elif token_file is not None:
            with open(token_file) as f:
                token = json.load(f)
                if "access_token" in token.keys():
                    headers.update({"Authorization": "Bearer " + token["access_token"]})
                else:
                    raise ValueError("'access_token' field missing in the file.")
        elif client_id is not None and client_secret is not None:
            headers.update({"clientId": client_id, "clientSecret": client_secret})
        else:
            raise ValueError("Please supply either authorization_token or client_id/client_secret parameters.")

        self.auth_url = auth_url
        self.headers = headers
        self.credentials = None
        self.item = None
        return

    def set_item(
            self,
            item_id: str,
            item_type: str,
            role: str):
        """
        Method to set the details of the Item to access

        Args:
            item_id (String): Id of the Item.
            item_type (String): Type of the Item.
            role (String): Role of the User.
        """
        self.item = {"itemId": item_id, "itemType": item_type, "role": role}
        return self

    def request_token(self) -> str:
        """
        Method to request a token for the private resources

        Returns:
             access_token (String): Token to access the private resources
        """
        if self.item is None:
            self.set_item("rs.iudx.org.in", "resource_server", "consumer")

        http_entity = HTTPEntity()
        url = self.auth_url + "/token"
        response: HTTPResponse = http_entity.post(url, json.dumps(self.item), self.headers)
        result_data = response.get_json()

        if response.get_status_code() == 200:
            self.credentials = result_data["results"]
            access_token = self.credentials["accessToken"]
            return access_token
        else:
            raise RuntimeError(result_data)
