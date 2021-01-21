import json

import pika

from pika_pika.consumers.config import connection_parameters
from pika_pika.consumers.consumer import Consumer


class JobConsumer(Consumer):
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
            print(message)

        except json.JSONDecodeError:
            return False

        return True


if __name__ == "__main__":
    job_consumer = JobConsumer(
        queue_name="test-queue",
        parameters=connection_parameters.parameters,
        exchange_name="test-exchange",
    )
    job_consumer.consume_forever()
