from functools import cached_property

import pika

from pika_pika.settings.settings import (
    RABBITMQ_HOST,
    RABBITMQ_PASSWORD,
    RABBITMQ_PORT,
    RABBITMQ_USERNAME,
    RABBITMQ_VIRTUAL_HOST,
)


class Credentials:
    def __init__(self, username: str, password: str):
        self._username: str = username
        self._password: str = password

    @cached_property
    def plain_credentials(self) -> pika.PlainCredentials:
        return pika.PlainCredentials(username=self._username, password=self._password)


class ConnectionParameters:
    def __init__(
        self,
        host: str,
        port: int,
        virtual_host: str,
        plain_credentials: pika.PlainCredentials,
    ):
        self._host: str = host
        self._port: int = port
        self._virtual_host: str = virtual_host
        self._plain_credentials: pika.PlainCredentials = plain_credentials

    @cached_property
    def parameters(self) -> pika.ConnectionParameters:
        return pika.ConnectionParameters(
            host=self._host,
            port=self._port,
            virtual_host=self._virtual_host,
            credentials=self._plain_credentials,
        )


credentials = Credentials(username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)

connection_parameters = ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    virtual_host=RABBITMQ_VIRTUAL_HOST,
    plain_credentials=credentials.plain_credentials,
)

if __name__ == "__main__":
    print(f"credentials: {credentials.plain_credentials}")
    print(f"connection_parameters: {connection_parameters.parameters}")
