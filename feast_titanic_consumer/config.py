import os

PUSH_SOURCE_NAME = os.getenv("PUSH_SOURCE_NAME", "titanic_passenger_push_source")
PUSH_SERVER_URL = os.getenv("PUSH_SERVER", "docker.for.mac.host.internal:6566")

BOOTSTRAP_SERVERS = [os.getenv("KAFKA_SERVER", "localhost:9092")]
KAFKA_TOPIC = os.getenv("TOPIC", "default")

BATCH_SIZE = 4
# seconds
TIMEOUT = 20
