import os
from feast import FileSource, KafkaSource
from feast.data_format import JsonFormat


KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_SERVER")

titanic_file_source = FileSource(path="data/titanic_train_file_source.parquet", timestamp_field="dummy_timestamp")

titanic_stream_source = KafkaSource(
    name="titanic_passenger_stream",
    kafka_bootstrap_servers="broker:29092",
    topic="passengers",
    timestamp_field="event_timestamp",
    batch_source=titanic_file_source,
    message_format=JsonFormat(schema_json="PassengerId integer, dummy_timestamp timestamp, Pclass double, Fare double"),
)
