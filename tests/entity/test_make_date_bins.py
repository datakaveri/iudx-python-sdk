import unittest
import json
import sys
sys.path.insert(1, './')
from iudx.entity.Entity import Entity
from iudx.auth.Token import Token

import pandas as pd
import zipfile
import os

from datetime import date, datetime, timedelta

from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery
from iudx.rs.ResourceResult import ResourceResult

class DateBinsTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DateBinsTest, self).__init__(*args, **kwargs)
        self.config = {}
        with open("./config.json", "r") as f:
            self.config = json.load(f)
        self.token_obj = Token(client_id=self.config["client_id"],
                            client_secret=self.config["client_secret"])
        self.time_format = "%Y-%m-%dT%H:%M:%SZ"

    def test_date_bins(self):
        e = Entity("datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/83cdf03d-5787-7052-08aa-143cfbfb807d", token_obj=self.token_obj)
        query = ResourceQuery().add_entity(
                    "datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/83cdf03d-5787-7052-08aa-143cfbfb807d").during_search("2021-12-18T00:00:00Z", "2021-12-29T00:00:00Z")
        date_bins = []
        start_time = datetime.strptime("2021-12-16T00:00:00Z", self.time_format)
        end_time = datetime.strptime("2021-12-27T00:00:00Z", self.time_format)
        e.make_date_bins(start_time, end_time, date_bins)
        for i in range(0, len(date_bins)-1):
            print(date_bins[i], date_bins[i+1])

        print(date_bins)
