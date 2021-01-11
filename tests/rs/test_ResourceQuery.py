'''
    This script creates a test user and display
'''
# import pytest
import unittest
import json
import sys
sys.path.insert(1, './')
from iudx.rs.ResourceQuery import ResourceQuery


class ResourceQueryTest(unittest.TestCase):
    """Test different scenarios for the ResourceQuery class.
    """
    def setUp(self):
        self.testVector = {}
        with open("./tests/rs/testVector_ResourceQuery.json", "r") as f:
            self.testVector = json.load(f)

        self.rs_entity = self.rs_query.add_entity(
            self.testVector["entities"][0]
            )

    def tearDown(self):
        pass

    def __init__(self, *args, **kwargs):
        """ResourceQueryTest base class constructor
        """
        super(ResourceQueryTest, self).__init__(*args, **kwargs)
        self.rs_query = ResourceQuery()

    def test_geo_search(self):
        """Function to test the geo search query.
        """
        print("*"*60)
        for geo_param in self.testVector["geo_params"]:
            result = self.rs_entity.during_search(
                start_time=self.testVector["temporal_params"][0]["start_time"],
                end_time=self.testVector["temporal_params"][0]["end_time"]
                ).geo_search(
                geoproperty=geo_param["geoproperty"],
                geometry=geo_param["geometry"],
                georel=geo_param["georel"],
                max_distance=geo_param["max_distance"],
                coordinates=geo_param["coordinates"]
                ).get_query()

            self.assertNotEqual(result, "")
            print(result, end="\n-----------\n")

    def test_during_search(self):
        """Function to test the temporal during search query.
        """
        print("*"*60)
        for time_param in self.testVector["temporal_params"]:
            result = self.rs_entity.during_search(
                start_time=time_param["start_time"],
                end_time=time_param["end_time"]
                ).get_query()

            self.assertNotEqual(result, "")
            print(result, end="\n-----------\n")

    def test_property_search(self):
        """Function to test the property search query.
        """
        print("*"*60)
        for property_param in self.testVector["property_params"]:
            result = self.rs_entity.during_search(
                start_time=self.testVector["temporal_params"][0]["start_time"],
                end_time=self.testVector["temporal_params"][0]["end_time"]
                ).property_search(
                key=property_param["key"],
                value=property_param["value"],
                operation=property_param["operation"]
                ).get_query()

            self.assertNotEqual(result, "")
            print(result, end="\n-----------\n")

    def test_add_filters(self):
        """Function to test the listed filter query.
        """
        print("*"*60)
        for filter_param in self.testVector["filters"]:
            result = self.rs_entity.add_filters(
                filters=filter_param,
                ).get_query()

            self.assertNotEqual(result, "")
            print(result, end="\n-----------\n")

    def test_complex_query(self):
        """Function to test the listed filter query.
        """
        print("*"*60)
        result = self.rs_entity.geo_search(
                geoproperty=self.testVector["geo_params"][0]["geoproperty"],
                geometry=self.testVector["geo_params"][0]["geometry"],
                georel=self.testVector["geo_params"][0]["georel"],
                max_distance=self.testVector["geo_params"][0]["max_distance"],
                coordinates=self.testVector["geo_params"][0]["coordinates"]
                ).during_search(
                start_time=self.testVector["temporal_params"][0]["start_time"],
                end_time=self.testVector["temporal_params"][0]["end_time"]
                ).property_search(
                key=self.testVector["property_params"][0]["key"],
                value=self.testVector["property_params"][0]["value"],
                operation=self.testVector["property_params"][0]["operation"]
                ).add_filters(
            filters=self.testVector["filters"][0],
            ).get_query()

        self.assertNotEqual(result, "")
        print(result, end="\n-----------\n")

    def test_latest_search(self):
        """Function to test the latest search query.
        """
        print("*"*60)
        result = self.rs_entity.latest_search()

        self.assertNotEqual(result, "")
        print(result, end="\n-----------\n")


if __name__ == '__main__':
    unittest.main()
