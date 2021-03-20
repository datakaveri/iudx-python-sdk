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
        self.latest: bool = True
        self.temporal: bool = False
        self.complex: bool = False
        self.apis_dict: dict = {"temporal": "/ngsi-ld/v1/temporal/entities",
                                "complex": "/ngsi-ld/v1/entityOperations/query",
                                "latest": "/ngsi-ld/v1/entities",
                                "subscription": "/ngsi-ld/v1/subscription"}
        self.entities: dict = {}
        return

    def add_entity(
            self,
            resource_id: str,
            api_list: list):
        """
        Method to add a private resource for which a token is required

        Args:
            resource_id (String): ID of the private resource to be accessed
            api_list (List of Strings): a list of the api capabailties required
                - 'subscription'
                - 'latest'
                - 'temporal'
                - 'complex'
        """
        apis = []
        if len(api_list):
            for api in api_list:
                if api in self.apis_dict:
                    apis.append(self.apis_dict[api])
                else:
                    raise RuntimeError(f"{api} is not a valid api")
        else:
            raise RuntimeError("api_list cannot be empty")
        self.entities[resource_id] = apis
        return

    def request_token(self) -> str:
        """
        Method to request a token for the added private resources

        Returns the token (String) to access added the private resources
        """
        data = {}
        requests = []
        for entity in self.entities.keys():
            request = {}
            request["id"] = entity
            request["apis"] = self.entities[entity]
            requests.append(request)
        data["request"] = requests
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
