from environs import Env

env = Env()
env.read_env()

RABBITMQ_HOST: str = env.str("RABBITMQ_HOST")
RABBITMQ_PASSWORD: str = env.str("RABBITMQ_PASSWORD")
RABBITMQ_PORT: int = env.int("RABBITMQ_PORT")
RABBITMQ_USERNAME: str = env.str("RABBITMQ_USERNAME")
RABBITMQ_VIRTUAL_HOST: str = env.str("RABBITMQ_VIRTUAL_HOST")
