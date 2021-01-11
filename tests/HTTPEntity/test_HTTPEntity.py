'''
    This script creates a test user and display
'''
import pytest
import unittest
import json
import sys
sys.path.insert(1, './')

from iudx.common.HTTPEntity import HTTPEntity
from iudx.common.HTTPResponse import HTTPResponse


class HTTPEntityTest(unittest.TestCase):
    """Test different scenarios for the HTTPEntity class.
    """

    def __init__(self, *args, **kwargs):
        """HTTPEntityTest base class constructor
        """
        super(HTTPEntityTest, self).__init__(*args, **kwargs)
        self.http_entity = HTTPEntity()

    def test_get(self):
        """Function to test the 'get' method for HTTPEntity.
        """
        self.testVector = {}
        with open("./tests/HTTPEntity/testVector_HTTPEntity.json", "r") as f:
            self.testVector = json.load(f)

        for param in self.testVector["params"]:
            result = self.http_entity.get(
                url=self.testVector["cat_url"] + "?" + param,
                headers=self.testVector["headers"])

            self.assertEqual(result.get_status_code(), 200)
            self.assertNotEqual(result.get_status_code(), 500)
            self.assertNotEqual(result.get_status_code(), 404)
            self.assertNotEqual(result.get_status_code(), 400)
            print(result.get_json())


if __name__ == '__main__':
    unittest.main()
