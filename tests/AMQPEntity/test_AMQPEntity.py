'''
    This script creates a test user and display
'''
import pytest
import unittest
import json
import sys
sys.path.insert(1, './')

from iudx.common.AMQPEntity import AMQPEntity
from iudx.common.AMQPResponse import AMQPResponse


class AMQPEntityTest(unittest.TestCase):
    """Test different scenarios for the AMQPEntity class.
    """

    def __init__(self, *args, **kwargs):
        """AMQPEntityTest base class constructor
        """
        super(AMQPEntityTest, self).__init__(*args, **kwargs)
        self.config = {}
        with open("./config.json", "r") as f:
            self.config = json.load(f)

        self.amqp_entity = AMQPEntity(
            username=self.config["streaming_config"]["sub_username"],
            password=self.config["streaming_config"]["password"],
            host=self.config["streaming_config"]["host"],
            port=self.config["streaming_config"]["port"],
            vhost=self.config["streaming_config"]["vhost"]
        )


    def test_subscribe(self):
        """Function to test the 'subscribe' method for AMQPEntity.
        """
        response: AMQPResponse = self.amqp_entity.subscribe('datakaveri.org/e3a0cd8b7cfcf2fdf065b4b0cb13131a174be66c/vadodaraAQM')
        
        
        

if __name__ == '__main__':
    unittest.main()
