'''
    This script creates a test user and display
'''
# import pytest
import unittest
import json
import sys
sys.path.insert(1, './')
from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery


class ResourceServerTest(unittest.TestCase):
    """Test different scenarios for the ResourceServer class.
    """
    def __init__(self, *args, **kwargs):
        """ResourceQueryTest base class constructor
        """
        super(ResourceServerTest, self).__init__(*args, **kwargs)

        self.testVector = {}
        with open("./tests/rs/testVector_ResourceServer.json", "r") as f:
            self.testVector = json.load(f)

        self.rs = ResourceServer(
            rs_url=self.testVector["url"],
            headers=self.testVector["headers"][0]
            )
        self.rs_query = ResourceQuery()

        self.rs_entity = self.rs_query.add_entity(
            self.testVector["entities"][0]
            )

    def test_get_latest(self):
        """Function to test the get latest resource API.
        """
        query = self.rs_entity
        result = self.rs.get_latest(query)

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
        query = self.rs_entity.geo_search(
                geoproperty=self.testVector["geo_params"][0]["geoproperty"],
                geometry=self.testVector["geo_params"][0]["geometry"],
                georel=self.testVector["geo_params"][0]["georel"],
                max_distance=self.testVector["geo_params"][0]["maxDistance"],
                coordinates=self.testVector["geo_params"][0]["coordinates"]
            ).during_search(
                start_time=self.testVector["time_params"][0]["time"],
                end_time=self.testVector["time_params"][0]["endtime"]
            )
        result = self.rs.get_data(query)

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
