'''
    This script creates a test user and display
'''
# import pytest
import unittest
import json
import sys
sys.path.insert(1, './')
from iudx.entity.Entity import Entity

import pandas as pd


class EntityTest(unittest.TestCase):
    """Test different scenarios for the Entity class.
    """
    def __init__(self, *args, **kwargs):
        """EntityTest base class constructor.
        """
        super(EntityTest, self).__init__(*args, **kwargs)

        self.testVector = {}
        with open("./tests/entity/testVector_Entity.json", "r") as f:
            self.testVector = json.load(f)
        self.entity = Entity(self.testVector["entity_ids"][0])

    def test_during_search(self):
        """Function to test the temporal during search query.
        """
        for time_param in self.testVector["temporal_params"]:
            df = self.entity.during_search(
                start_time=time_param["start_time"],
                end_time=time_param["end_time"]
            )

            self.assertNotEqual(df.shape[0], 0)
            self.assertGreaterEqual(df.shape[0], 1)
            self.assertIsNotNone(df)
            self.assertIsInstance(df, pd.DataFrame)

        print("*"*60 + "\n" + "*"*60)
        print(
            f"DataFrame has {df.shape[0]} rows and {df.shape[1]} columns.",
            end="\n-----------\n"
            )
        print(f"Columns in DataFrame:\n{df.columns}", end="\n-----------\n")
        print(df.head)
        print("*"*60)


if __name__ == '__main__':
    unittest.main()
