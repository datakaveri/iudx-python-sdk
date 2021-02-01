"""Module doc string. Leave empty for now.

ResourceServer.py
"""

from typing import TypeVar, Generic, Any, List, Dict

from iudx.common.HTTPEntity import HTTPEntity
from iudx.common.HTTPResponse import HTTPResponse

from iudx.rs.ResourceQuery import ResourceQuery
from iudx.rs.ResourceResult import ResourceResult
import json
import multiprocessing
from multiprocessing import Process, Pool


class ResourceServer():
    """Abstract class for Resource Server. Helps to create a modular
       interface for the API to implement queries.
    """

    def __init__(self, rs_url: str=None, token: str=None,
                 headers: Dict[str, str]=None):
        """ResourceServer base class constructor
        """
        self.url: str = rs_url
        self.token: str = token
        self.headers: Dict[str, str] = headers

        if self.token is not None:
            self.headers["token"] = self.token
        return

    def status(self) -> bool:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def get_data(self, queries: List[ResourceQuery]) -> List[ResourceResult]:
        """Method to post the request for geo, temporal, property, add filters
            and make complex query.

        Args:
            queries (List[ResourceQuery]): A list of query objects of 
            ResourceQuery class.
        Returns:
            rs_results (List[ResourceResult]): returns a list of 
                ResourceResult object.
        """
        url = self.url + "/entityOperations/query"
        pool = Pool(processes=multiprocessing.cpu_count())

        zipped_url = []
        for query in queries:
            zipped_url.append((url, query.get_query(), self.headers))

        responses: List[HTTPResponse] = pool.starmap(
            HTTPEntity().post,
            zipped_url
            )

        rs_results = []
        for response in responses:
            rs_result = ResourceResult()

            if response.get_status_code() == 401:
                raise RuntimeError("Not Authorized: Invalid Credentials")

            elif response.get_status_code() == 200:
                result_data = response.get_json()
                rs_result.type = result_data["type"]
                rs_result.title = result_data["title"]
                rs_result.results = result_data["results"]
                rs_results.append(rs_result)

        return rs_results

    def get_latest(self, query: ResourceQuery) -> ResourceResult:
        """Method to get the request for latest resource data.

        Args:
            query (ResourceQuery): A query object of ResourceQuery class.
        Returns:
            rs_result (ResourceResult): returns a ResourceResult object.
        """
        url = self.url + "/entities"
        url = url + query.latest_search()
        http_entity = HTTPEntity()
        response: HTTPResponse = http_entity.get(
            url,
            self.headers
            )
        result_data = response.get_json()

        rs_result = ResourceResult()
        if response.get_status_code() == 200:
            rs_result.type = result_data["type"]
            rs_result.title = result_data["title"]
            rs_result.results = result_data["results"]
        else:
            rs_result.type = result_data["type"]
            rs_result.title = result_data["title"]
        return rs_result
