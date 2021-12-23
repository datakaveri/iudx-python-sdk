"""Module doc string. Leave empty for now.

ResourceServer.py
"""
import json
import datetime
import dateutil.parser
from typing import TypeVar, Generic, Any, List, Dict

from iudx.common.HTTPEntity import HTTPEntity
from iudx.common.HTTPResponse import HTTPResponse

from iudx.rs.ResourceQuery import ResourceQuery
from iudx.rs.ResourceResult import ResourceResult

from iudx.auth.Token import Token

import multiprocessing


class ResourceServer():
    """Abstract class for Resource Server. Helps to create a modular
       interface for the API to implement queries.
    """

    def __init__(self, rs_url: str=None, token: str=None, token_obj: Token=None,
                 headers: Dict[str, str]=None):
        """ResourceServer base class constructor
        """
        # Request access token
        if token is None and token_obj is not None:
            token = token_obj.request_token()

        self.url: str = rs_url
        self.token: str = token
        self.headers: Dict[str, str] = headers
        self.pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

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

    def parse_response(self, responses: List[HTTPResponse]) -> List[ResourceResult]:
        """Parse responses

       Args:
           responses (argument-type): response fetched for the query
       Returns:
           parsed response
       """
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
                rs_result.offset = result_data["offset"]
                rs_result.limit = result_data["limit"]
                rs_result.totalHits = result_data["totalHits"]
                rs_results.append(rs_result)

        return rs_results

    def get_all_data(self, rs_results: List[ResourceResult], url: str, queries: List[ResourceQuery]):
        """Helper method for fetching all the data between the time range.

            Loops through all offsets and get the data automatically

       Args:
           rs_results (List[ResourceResult]): results returned from the previous request (first 5000 hits)
           url (str): request url
           queries (List[ResourceQuery]): A list of query objects of ResourceQuery class.
       Returns:
           results for all the data fetched
       """

        total_hits = rs_results[0].totalHits
        limit = rs_results[0].limit # default 5000
        offset_window = int(total_hits / limit)

        for i in range(offset_window):
            zipped_url = []
            for query in queries:
                new_url = url + "?offset=" + str(limit * (i + 1)) + "&limit=" + str(limit)
                zipped_url.append((new_url, query.get_query(), self.headers))

            responses: List[HTTPResponse] = self.pool.starmap(
                HTTPEntity().post,
                zipped_url
            )
            rs_results = rs_results + self.parse_response(responses)

        return rs_results

    def get_data_recursively(self, start_time: str, end_time: str, url: str, queries: List[ResourceQuery]):
        """Helper method for recursively fetch data between the time range

            Since the maximum offset for fetching data is 49999, the range which contains more totalHits will be
            chunked into various time ranges recursively and data is fetched for all time ranges.

       Args:
           start_time (str): The starting timestamp for the search.
           end_time (str): The ending timestamp for the search.
           url (str): request url
           queries (List[ResourceQuery]): A list of query objects of ResourceQuery class.
       Returns:
           results for all the data fetched
       """

        new_start_time = dateutil.parser.isoparse(start_time)
        new_end_time = dateutil.parser.isoparse(end_time)

        if new_start_time >= new_end_time:
            return []

        zipped_url = []
        for query in queries:
            query.during_search(start_time, end_time)
            new_query = query.get_query()
            zipped_url.append((url, new_query, self.headers))

        responses: List[HTTPResponse] = self.pool.starmap(
            HTTPEntity().post,
            zipped_url
        )

        results = self.parse_response(responses)
        if len(results) == 0:
            return []

        total_hits = results[0].totalHits
        if total_hits < 5000:
            return results
        elif total_hits < 50000:
            return results + self.get_all_data(results, url, queries)

        new_mid_time = new_start_time + (new_end_time - new_start_time) / 2
        final_mid_time = new_mid_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        next_mid_time = (new_mid_time + datetime.timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

        results += self.get_data_recursively(start_time, final_mid_time, url, queries)
        results += self.get_data_recursively(next_mid_time, end_time, url, queries)
        return results

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
        url = self.url + "/temporal/entityOperations/query"

        rs_results = []
        zipped_url = []
        offset = None
        limit = None
        start_time = None
        end_time = None
        for query in queries:
            offset, limit = query.get_offset_limit()
            new_query = query.get_query()
            query_obj = json.loads(new_query)
            start_time = query_obj['temporalQ']['time']
            end_time = query_obj['temporalQ']['endtime']
            new_url = url
            if offset is not None and limit is not None:
                new_url = url + "?offset=" + str(offset) + "&limit=" + str(limit)
            zipped_url.append((new_url, new_query, self.headers))

        if offset is not None and limit is not None:
            responses: List[HTTPResponse] = self.pool.starmap(
                HTTPEntity().post,
                zipped_url
                )

            rs_results = self.parse_response(responses)
        elif start_time is not None and end_time is not None:
            rs_results = self.get_data_recursively(start_time, end_time, url, queries)

        return rs_results

    def get_latest(self, queries: List[ResourceQuery]) -> List[ResourceResult]:
        """Method to get the request for latest resource data.

        Args:
            query (ResourceQuery): A query object of ResourceQuery class.
        Returns:
            rs_result (ResourceResult): returns a ResourceResult object.
        """
        base_url = self.url + "/entities"

        zipped_url = []
        for query in queries:
            url = base_url + query.latest_search()
            zipped_url.append((url, self.headers))

        responses: List[HTTPResponse] = self.pool.starmap(
            HTTPEntity().get,
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
