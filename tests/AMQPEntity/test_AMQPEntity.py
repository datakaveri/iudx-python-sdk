'''
    This script creates a test user and display
'''
import pytest
import unittest
import json
import sys
import time
sys.path.insert(1, './')

from iudx.common.AMQPEntity import AMQPEntity
# from iudx.common.AMQPResponse import AMQPResponse


class AMQPEntityTest(unittest.TestCase):
    """Test different scenarios for the AMQPEntity class.
    """
    def callback(self, ch, method, properties, body):
        print(body)

    def __init__(self, *args, **kwargs):
        """AMQPEntityTest base class constructor
        """
        super(AMQPEntityTest, self).__init__(*args, **kwargs)
        self.config = {}
        with open("./config.json", "r") as f:
            self.config = json.load(f)

       
    def test_subscribe(self):
        """Function to test the 'subscribe' method for AMQPEntity.
        """
        self.amqp_entity = AMQPEntity(
            username=self.config["streaming_config"]["sub_username"],
            password=self.config["streaming_config"]["password"],
            host=self.config["streaming_config"]["host"],
            port=self.config["streaming_config"]["port"],
            vhost=self.config["streaming_config"]["vhost"]
        )
        self.amqp_entity.set_callback(self.callback)
        self.amqp_entity.subscribe('datakaveri.org/f5443e47d00ad616b2f8bb4f116e4c9fe88e4835/ITMS-Analytics-Live')
        while(True):
            
            time.sleep(5)

if __name__ == '__main__':
    unittest.main()