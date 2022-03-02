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

class QueryBatchTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(QueryBatchTest, self).__init__(*args, **kwargs)
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

    def test_batches_resource(self):
        e = Entity("datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/83cdf03d-5787-7052-08aa-143cfbfb807d", token_obj=self.token_obj)
        query = ResourceQuery().add_entity(
                    "datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/83cdf03d-5787-7052-08aa-143cfbfb807d").during_search("2021-12-18T00:00:00Z", "2021-12-29T00:00:00Z")
        batch_queries = []
        e.make_query_batches(query, batch_queries)
        for q in batch_queries:
            print(q.get_query())
