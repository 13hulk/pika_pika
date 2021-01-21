import json

import pika

from pika_pika.consumers.config import connection_parameters
from pika_pika.consumers.consumer import Consumer


class ExampleConsumer(Consumer):
    def __init__(
        self,
        queue_name: str,
        parameters: pika.ConnectionParameters,
        exchange_name: str,
    ):
        super().__init__(
            queue_name=queue_name, parameters=parameters, exchange_name=exchange_name,
        )

    def callback(self, message: str, method: pika.spec.Basic.GetOk) -> bool:
        """
        Abstract Method implementation.
        """
        try:
            message = json.loads(message)
            print(f"Message: {message}")
        except json.JSONDecodeError:
            print(f"Message: {message}")

        return True


if __name__ == "__main__":
    example_consumer = ExampleConsumer(
        queue_name="example-queue",
        parameters=connection_parameters.parameters,
        exchange_name="example-exchange",
    )
    example_consumer.consume_forever()
