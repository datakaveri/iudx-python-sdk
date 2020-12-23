'''
    This script creates a test user and display
'''
# import pytest
import unittest
import json
import sys
sys.path.insert(1, './')
from iudx.cat.CatalogueQuery import CatalogueQuery


class CatalogueQueryTest(unittest.TestCase):
    """Test different scenarios for the CatalogueQuery class.
    """
    def setUp(self):
        self.testVector = {}
        with open("./tests/cat/testVector_CatalogueQuery.json", "r") as f:
            self.testVector = json.load(f)

    def tearDown(self):
        pass

    def __init__(self, *args, **kwargs):
        """CatalogueQueryTest base class constructor
        """
        super(CatalogueQueryTest, self).__init__(*args, **kwargs)
        self.cat_query = CatalogueQuery()

    def test_geo_search(self):
        """Function to test the geo search query.
        """
        for geo_param in self.testVector["geo_params"]:
            result = self.cat_query.geo_search(
                geoproperty=geo_param["geoproperty"],
                geometry=geo_param["geometry"],
                georel=geo_param["georel"],
                max_distance=10000,
                coordinates=geo_param["coordinates"]
                ).get_query()

            self.assertNotEqual(result, "")
            print(result, end="\n******************\n")

    def test_property_search(self):
        """Function to test the property search query.
        """
        for property_param in self.testVector["property_params"]:
            result = self.cat_query.property_search(
                key=property_param["key"],
                value=property_param["value"],
                ).get_query()

            self.assertNotEqual(result, "")
            print(result, end="\n******************\n")

    def test_text_search(self):
        """Function to test the text search query.
        """
        for text_param in self.testVector["text_params"]:
            result = self.cat_query.text_search(
                text_query=text_param
                ).get_query()

            self.assertNotEqual(result, "")
            self.assertGreater(len(result), 2)
            self.assertLess(len(result), 103) 
            print(result, end="\n******************\n")

    def test_filter_search(self):
        """Function to test the filter search query.
        """
        for filter_param in self.testVector["filter_params"]:
            result = self.cat_query.add_filters(
                filters=filter_param["filter_list"]
                ).get_query()

            self.assertNotEqual(result, "")
            print(result, end="\n******************\n")

    def test_get_query(self):
        """Function to test the query generator method.
        """
        result = self.cat_query.geo_search(
            geoproperty=self.testVector["geo_params"][0]["geoproperty"],
            geometry=self.testVector["geo_params"][0]["geometry"],
            georel=self.testVector["geo_params"][0]["georel"],
            max_distance=10000,
            coordinates=self.testVector["geo_params"][0]["coordinates"]
            ).property_search(
            key=self.testVector["property_params"][0]["key"],
            value=self.testVector["property_params"][0]["value"],
            ).text_search(
            text_query=self.testVector["text_params"][0]
            ).add_filters(
            filters=self.testVector["filter_params"][0]["filter_list"]
            ).get_query()

        self.assertNotEqual(result, "")
        print(result, end="\n****************\n******************\n")


if __name__ == '__main__':
    unittest.main()
