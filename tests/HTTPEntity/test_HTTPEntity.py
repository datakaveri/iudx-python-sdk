'''
    This script creates a test user and display
'''
import pytest
import unittest
import json
import sys
sys.path.insert(1, './')

from iudx.common.HTTPEntity import HTTPEntity


class HTTPEntityTest(unittest.TestCase):
    ''' Test different scenarios '''

    def __init__(self, *args, **kwargs):
        super(HTTPEntityTest, self).__init__(*args, **kwargs)
        self.http_entity = HTTPEntity({"demoCert": "123"})

    def test_get(self):

        self.testVector = {}
        with open("./tests/catalogue/testVector_HTTPEntity.json", "r") as f:
            self.testVector = json.load(f)

        result = self.http_entity.get(
            url=self.testVector["prod_urls"][0],
            path_params=self.testVector["params"][0],
            headers=self.testVector["headers"][0])

        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(result.status_code, 500)
        self.assertNotEqual(result.status_code, 404)
        self.assertNotEqual(result.status_code, 400)

        # print(result.json())


if __name__ == '__main__':
    unittest.main()
    