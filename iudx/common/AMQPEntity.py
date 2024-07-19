"""Module doc string. Leave empty for now.

AMQPEntity.py
"""

from typing import TypeVar, Dict
from iudx.common.AMQPResponse import AMQPResponse
import json
import pika
import urllib.parse

AMQPEntity = TypeVar('T')


class AMQPEntity():
    """Abstract class for subscription.
    """

    def __init__(self, username:str=None, 
                 password:str=None, host:str=None, 
                 port:int=None, vhost:str=None):
        """AMQPEntity base class constructor

        Args:
            
        """
        self.sub_username: str = username
        self.password: str = password
        self.host: str = host
        self.vhost: str = vhost
        self.port : int = port
        self.callback = None
        return



    def subscribe(self, queue_name:str):
        """Method to subscribe to a stream of data.

        Args:
            queue_name(String): Queue name for AMQP Streaming
        Returns:
            response (AMQPResponse): AMQP Response after the subscription.
        """
        username = urllib.parse.quote_plus(self.sub_username)        
        connection = pika.BlockingConnection(pika.URLParameters(f"amqps://{username}:{self.password}@{self.host}:{str(self.port)}/{self.vhost}"))
        channel = connection.channel()
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()

    def set_callback(self, callback):
        """Method to subscribe to a stream of data.

        Args:
        
        Returns:
            response (AMQPResponse): AMQP Response after the subscription.
        """
        self.callback = callback
    



     