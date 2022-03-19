import unittest
import json
import sys
sys.path.insert(1, './')
from iudx.entity.Entity import Entity
from iudx.auth.Token import Token

import pandas as pd
import zipfile
import os

from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery
from iudx.rs.ResourceResult import ResourceResult

class DuringTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DuringTest, self).__init__(*args, **kwargs)
        self.config = {}
        with open("./config.json", "r") as f:
            self.config = json.load(f)
        self.token_obj = Token(client_id=self.config["client_id"],
                            client_secret=self.config["client_secret"])


        rs_url ="https://rs.iudx.org.in/ngsi-ld/v1"
        headers =  {"content-type": "application/json"}
        self.rs: ResourceServer = ResourceServer(
            rs_url=rs_url,
            headers=headers,
            token_obj=self.token_obj
        )

    def test_get_static_data(self):
        iid = "varanasismartcity.gov.in/62d1f729edd3d2a1a090cb1c6c89356296963d55/rs.iudx.org.in/varanasi-point-of-interests/smartpole-locations"
        e = Entity(iid, token_obj=self.token_obj)
        df = e.property_search("id", iid, operation="==")
        print(df.shape)
