'''
    This script creates a test user and display
'''
# import pytest
import unittest
import sys
sys.path.insert(1, './')

from iudx.common.HTTPEntity import HTTPEntity


class HTTPEntityTest(unittest.TestCase):
    ''' Test different scenarios '''

    def __init__(self, *args, **kwargs):
        super(HTTPEntityTest, self).__init__(*args, **kwargs)
        self.http_entity = HTTPEntity({"abc": "123"})

    def test_get(self):
        result = self.http_entity.get(
            url="https://jsonplaceholder.typicode.com/todos/1",
                                   path_params={"tags": ["flood"]},
                                   headers={"tags": "fds"})

        self.assertNotEqual(result.status_code, 400)
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
    