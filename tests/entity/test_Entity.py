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
import zipfile
import os


class EntityTest(unittest.TestCase):
    """Test different scenarios for the Entity class.
    """
    def __init__(self, *args, **kwargs):
        """EntityTest base class constructor.
        """
        super(EntityTest, self).__init__(*args, **kwargs)

        self.config = {}
        with open("./config.json", "r") as f:
            self.config = json.load(f)

        self.testVector = {}
        with open("./tests/entity/testVector_Entity.json", "r") as f:
            self.testVector = json.load(f)

    def test_latest(self):
        """Function to test the latest search query.
        """

        for e in self.testVector["entity_ids"]:
            self.entity = Entity(e)

            for time_param in self.testVector["temporal_params"]:
                df = self.entity.latest()

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

    def test_during_search(self):
        """Function to test the temporal during search query.
        """

        for e in self.testVector["entity_ids"]:
            self.entity = Entity(e, token=self.config["headers"]["token"])

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

    def test_download(self):
        """Function to test the downloading of file in csv format.
        """
        file_name = "test_download_file"

        for e in self.testVector["entity_ids"]:
            self.entity = Entity(e, token=self.config["headers"]["token"])

            for time_param in self.testVector["temporal_params"]:
                df = self.entity.during_search(
                    start_time=time_param["start_time"],
                    end_time=time_param["end_time"]
                )

                self.assertNotEqual(df.shape[0], 0)
                self.assertGreaterEqual(df.shape[0], 1)
                self.assertIsNotNone(df)
                self.assertIsInstance(df, pd.DataFrame)
            
            for file_type in self.testVector["file_types"]:
                self.entity.download(file_name, file_type)

                zf = zipfile.ZipFile(f"{file_name}.zip")
                
                if file_type == "csv":
                    df_csv = pd.read_csv(zf.open(f"{file_name}.{file_type}"))
                    self.assertIsNotNone(df_csv)
                    self.assertIsInstance(df_csv, pd.DataFrame)
                    os.remove(f"{file_name}.zip")

                elif file_type == "json":
                    df_json = pd.read_json(zf.open(f"{file_name}.{file_type}"), orient='records')
                    self.assertIsNotNone(df_json)   
                    self.assertIsInstance(df_json, pd.DataFrame)      
                    os.remove(f"{file_name}.zip")           
                
                else:
                    raise RuntimeError(f"File type '{file_type}' is not supported.")


if __name__ == '__main__':
    unittest.main()
