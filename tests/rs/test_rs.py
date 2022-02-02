'''
    This script creates a test user and display
'''
# import pytest
import unittest
import json
import sys
sys.path.insert(1, './')
from typing import TypeVar, Generic, Any, List, Dict

from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery
from iudx.rs.ResourceResult import ResourceResult


class ResourceServerTest(unittest.TestCase):
    """Test different scenarios for the ResourceServer class.
    """
    def __init__(self, *args, **kwargs):
        """ResourceQueryTest base class constructor
        """
        super(ResourceServerTest, self).__init__(*args, **kwargs)

        # self.config = {}
        # with open("./config.json", "r") as f:
        #     self.config = json.load(f)

        self.testVector = {}
        with open("testVector_ResourceServer.json", "r") as f:
            self.testVector = json.load(f)

        # self.rs = ResourceServer(
        #     rs_url=self.config["urls"]["rs_url"],
        #     headers=self.config["headers"],
        #     )

        self.rs = ResourceServer(
            rs_url="https://rs.iudx.org.in/ngsi-ld/v1",
            headers={"content-type": "application/json",
                     "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiIyOWVjNGZjOS03NDVhLTQyNjEtOTA3My02YTI5OGE3ZjQwZGUiLCJpc3MiOiJhdXRob3JpemF0aW9uLml1ZHgub3JnLmluIiwiYXVkIjoicnMuaXVkeC5vcmcuaW4iLCJleHAiOjE2NDM4MjMxMzYsImlhdCI6MTY0Mzc3OTkzNiwiaWlkIjoicmk6ZGF0YWthdmVyaS5vcmcvMDRhMTVjOTk2MGZmZGEyMjdlOTU0NmYzZjQ2ZTYyOWUxZmU0MTMyYi9ycy5pdWR4Lm9yZy5pbi9wdW5lLWVudi1hcW0vZjM2YjQ2NjktNjI4Yi1hZDkzLTk5NzAtZjlkNDI0YWZiZjc1Iiwicm9sZSI6ImNvbnN1bWVyIiwiY29ucyI6eyJhY2Nlc3MiOlsic3ViIl19fQ.A4nDWVB_7YCSHWfDlMb2ERK4Oy1s8VQsR-b2DBxv6gKMpi5DMOVG3kRMJrkCL--MUryWZ-BtwY0cXwgJcTxTqw"
                     }
        )

        self.rs_query = ResourceQuery()

        self.rs_entity = self.rs_query.add_entity(
            self.testVector["entities"][0]
            )

    def test_get_latest(self):
        """Function to test the get latest resource API.
        """
        querries = []
        for i in range(3):
            query = self.rs_entity
            querries.append(query)

        results: List[ResourceResult] = self.rs.get_latest(querries)

        for result in results:
            print(f"RESULTS: {result.results}")
            print(f"TYPE: {result.type}")
            print(f"TITLE: {result.title}")
            print("*"*30)

            self.assertEqual(result.type, 200)
            self.assertNotEqual(result.type, 400)
            self.assertNotEqual(result.type, 401)
            self.assertNotEqual(result.type, 404)
            self.assertNotEqual(result.type, 415)
            self.assertNotEqual(result.type, 500)

    def test_get_data(self):
        """Function to test the post complex query response API.
        """
        querries = []
        for i in range(3):
            query = self.rs_entity.during_search(
                    start_time=self.testVector["time_params"][i]["time"],
                    end_time=self.testVector["time_params"][i]["endtime"]
                )
            querries.append(query)

        results: List[ResourceResult] = self.rs.get_data(querries)

        for result in results:
            print("*"*30)
            print("*"*30)
            print(results)
            print("*"*30)

            print(f"RESULTS: {result.results}")
            print(f"TYPE: {result.type}")
            print(f"TITLE: {result.title}")
            print("*"*30)

            self.assertEqual(result.type, 200)
            self.assertNotEqual(result.type, 400)
            self.assertNotEqual(result.type, 401)
            self.assertNotEqual(result.type, 404)
            self.assertNotEqual(result.type, 415)
            self.assertNotEqual(result.type, 500)


if __name__ == '__main__':
    unittest.main()
