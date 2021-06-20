from requests import Request, Session
import json


class Token():
    """
    Provides token functionality for accessing
    single private resources
    """

    def __init__(
            self,
            cert: str = None,
            key: str = None,
            auth_url: str = "https://authorization.iudx.org.in/auth/v1/token",
            headers: dict = {"content-type": "application/json"}):
        """
        Token class constructor for requesting tokens

        Args:
            cert (String): path to the certificate
            key (String): path to the private key
        """
        self.cert = cert
        self.key = key
        self.auth_url = auth_url
        self.headers = headers
        self.token: str = None
        self.token_response: dict = None
        self.entities: list = []
        return

    def add_entity(
            self,
            resource_ids: list
        ):
        """
        Method to add a private resource for which a token is required

        Args:
            resource_id (List): IDs of the private resources to be accessed
        """
        self.entities.extend([i for i in resource_ids if i not in self.entities])
        return
    
    def view_entities(self):
        """
        Method to view the entitiy ids added
        """
        if self.entities:
            print(self.entities)
        else:
            print("No entites added")
        return
    
    def remove_entity(
            self,
            resource_ids: list
        ):
        """
        Method to remove added entities
        
        Args:
            resource_ids (List): IDs to be removed
        """
        for i in resource_ids:
            self.entities.remove(i)
        return

    def request_token(self) -> str:
        """
        Method to request a token for the added private resources

        Returns the token (String) to access added the private resources
        """
        data = {}
        data["request"] = self.entities
        
        s = Session()
        request = Request('POST',
                          url=self.auth_url,
                          data=json.dumps(data),
                          headers=self.headers
                          )
        prepared_req = request.prepare()

        response = s.send(prepared_req,
                          cert=(self.cert, self.key))
        if response.status_code == 200:
            self.token_response = json.loads(response.text)
            self.token = self.token_response['token']
            return self.token
        else:
            raise RuntimeError(response.text)
