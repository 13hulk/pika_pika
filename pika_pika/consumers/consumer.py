import time
from abc import ABC, abstractmethod
from typing import Union

import pika


class Consumer(ABC):
    WAIT_PERIOD: int = 30

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
        if (
            self._connection is None
            or self._connection.is_closed
            or not self._connection.is_open
        ):
            self._connection = pika.BlockingConnection(self._parameters)

        return self._connection

    @property
    def channel(self) -> pika.adapters.blocking_connection.BlockingChannel:
        if (
            self._channel is None
            or self._channel.is_closed
            or not self._channel.is_open
        ):
            self._channel = self.connection.channel()

            self.channel.exchange_declare(
                exchange=self._exchange_name, exchange_type=self._exchange_type
            )
            self.channel.queue_declare(queue=self._queue_name, durable=True)
            self.channel.queue_bind(
                exchange=self._exchange_name,
                queue=self._queue_name,
                routing_key=self._queue_name,
            )
            self.channel.basic_qos(prefetch_count=1)

        return self._channel

    def _acknowledge(self, method: pika.spec.Basic.GetOk):
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        # Handle this manually.
        method, _, body = self.channel.basic_get(queue=self._queue_name)
        # TODO: For elegant code, experiment with `channel.basic_consume()` instead.

        # No message
        if method is None:
            time.sleep(self.WAIT_PERIOD)
            return

        # else:
        success = self.callback(message=body, method=method)

        # Acknowledge only if the callback was successful.
        # BTW, don't take this philosophically!
        if success is True:
            self._acknowledge(method=method)

    def consume_forever(self):
        while True:
            try:
                self.consume()

            except KeyboardInterrupt:
                # Destroy the connection when killed by the user!
                print(
                    f"KeyboardInterrupt: Gracefully closing the connection and shutting down"
                    + f" | Consumer: {self.__class__.__name__}"
                )
                self.connection.close()
                break

            except Exception as error:
                # Retry
                continue

    @abstractmethod
    def callback(self, message: str, method: pika.spec.Basic.GetOk) -> bool:
        """
        Derived class must implement this.
        """
        pass
