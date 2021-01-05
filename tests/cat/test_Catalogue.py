'''
    This script creates a test user and display
'''
# import pytest
import unittest
import json
import sys
sys.path.insert(1, './')
from iudx.cat.Catalogue import Catalogue
from iudx.cat.CatalogueQuery import CatalogueQuery


class CatalogueTest(unittest.TestCase):
    """Test different scenarios for the Catalogue class.
    """
    def setUp(self):
        self.testVector = {}
        with open("./tests/cat/testVector_Catalogue.json", "r") as f:
            self.testVector = json.load(f)

    def tearDown(self):
        pass

    def __init__(self, *args, **kwargs):
        """CatalogueTest base class constructor
        """
        super(CatalogueTest, self).__init__(*args, **kwargs)
        self.cat = Catalogue(
            cat_url="https://api.catalogue.iudx.io/iudx/cat/v1",
            headers={"content-type": "application/json"}
            )
        self.cat_query = CatalogueQuery()

    def test_search_entity(self):
        """Function to test the search entity query.
        """
        for entity in self.testVector["text_params"]:
            query = self.cat_query.text_search(entity)
            result = self.cat.search_entity(query)
            print(f"DOCUMENTS: {result.documents}")
            print(f"STATUS: {result.status}")
            print(f"TOTAL HITS: {result.total_hits}")
            print("*"*30)

    def test_count_entity(self):
        """Function to test the count entity query.
        """
        for entity in self.testVector["text_params"]:
            query = self.cat_query.text_search(entity)
            result = self.cat.count_entity(query)
            print(f"DOCUMENTS: {result.documents}")
            print(f"STATUS: {result.status}")
            print(f"TOTAL HITS: {result.total_hits}")
            print("*"*30)

    def test_list_entity(self):
        """Function to test the list entity query.
        """
        for entity in self.testVector["entity_type"]:
            result = self.cat.list_entity(entity)
            print(f"DOCUMENTS: {result.documents}")
            print(f"STATUS: {result.status}")
            print(f"TOTAL HITS: {result.total_hits}")
            print("*"*30)

    def test_related_entity(self):
        """Function to test the related entity query.
        """
        for entity in self.testVector["related_entity"]:
            result = self.cat.get_related_entity(entity[0], entity[1])
            print(f"DOCUMENTS: {result.documents}")
            print(f"STATUS: {result.status}")
            print(f"TOTAL HITS: {result.total_hits}")
            print("*"*30)


if __name__ == '__main__':
    unittest.main()
