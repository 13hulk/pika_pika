import json
import traceback
from abc import ABC
from functools import cached_property
from typing import Union

import pika

from pika_pika.consumers.config import connection_parameters


class Producer(ABC):
    def __init__(
        self,
        queue_name: str,
        parameters: pika.ConnectionParameters,
        exchange_name: str,
    ):
        self._queue_name: str = queue_name

        self._parameters: pika.ConnectionParameters = parameters
        self._exchange_name: str = exchange_name
        self._exchange_type: str = "direct"
        self._channel: Union[
            pika.adapters.blocking_connection.BlockingChannel, None
        ] = None
        self._connection: Union[pika.BlockingConnection, None] = None

    @property
    def connection(self) -> pika.BlockingConnection:
        if self._connection is None or self._connection.is_closed:
            print(f"Creating the connection...")
            self._connection = pika.BlockingConnection(self._parameters)

        return self._connection

    @property
    def channel(self) -> pika.adapters.blocking_connection.BlockingChannel:
        if self._channel is None or self._channel.is_closed:
            print(f"Creating the channel...")
            self._channel = self.connection.channel()

            print(f"Declaring the exchange...")
            self._channel.exchange_declare(
                exchange=self._exchange_name, exchange_type=self._exchange_type
            )
            print(f"Declaring the queue...")
            self._channel.queue_declare(queue=self._queue_name, durable=True)
            self._channel.queue_bind(
                exchange=self._exchange_name,
                queue=self._queue_name,
                routing_key=self._queue_name,
            )

        return self._channel

    @cached_property
    def properties(self) -> pika.BasicProperties:
        return pika.BasicProperties(
            delivery_mode=2, content_type="application/json",  # Make message persistent
        )

    def publish(self, message: Union[dict, str]):
        if isinstance(message, dict):
            message = json.dumps(message)
        try:
            self.channel.basic_publish(
                exchange=self._exchange_name,
                routing_key=self._queue_name,
                body=message,
                properties=self.properties,
            )
            print("Message published to the queue.")
            return True

        except Exception as error:
            print(
                f"{error.__class__.__name__} while publishing the message to the queue."
            )
            traceback.print_exc()
            return False


if __name__ == "__main__":
    ai_test_producer = Producer(
        queue_name="test-queue",
        parameters=connection_parameters.parameters,
        exchange_name="test-exchange",
    )
    ai_test_producer.publish(
        message={
            "Message": f"This is your posterity. All I have for you is a word: TENET"
        }
    )
