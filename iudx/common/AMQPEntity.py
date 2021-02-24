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
        return



    def subscribe(self, queue_name:str) -> AMQPResponse:
        """Method to subscribe to a stream of data.

        Args:
            config (method): Contains all the credential and topic information .
            Callback (method): Callback function for PIKA subscription.
        Returns:
            response (AMQPResponse): AMQP Response after the subscription.
        """

        def callback(self, ch, method, properties, body) -> AMQPResponse:
            """Method to subscribe to a stream of data.

            Args:
            
            Returns:
                response (AMQPResponse): AMQP Response after the subscription.
            """
            response = AMQPResponse()
            AMQPResponse()._response = body
            return response

        username = urllib.parse.quote_plus(self.sub_username)        
        connection = pika.BlockingConnection(pika.URLParameters(f"amqps://{username}:{self.password}@{self.host}:{str(self.port)}/{self.vhost}"))
        channel = connection.channel()
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()


        
    


     