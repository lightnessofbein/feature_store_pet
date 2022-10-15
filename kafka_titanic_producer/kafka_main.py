import json
from datetime import datetime

import pandas as pd
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
import os

BOOTSTRAP_SERVERS = [os.getenv("KAFKA_SERVER", "ERROR")]
TOPIC = os.getenv("TOPIC")


def create_stream(topic_name):
    topic_name = topic_name

    producer = None
    admin = None
    try:
        producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
        admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
        print("SUCCESS: instantiated Kafka admin and producer")
    except Exception as e:
        print(f"ERROR instantiating admin and producer with bootstrap servers {BOOTSTRAP_SERVERS} \n {e}")

    try:
        # Create Kafka topic
        topic = NewTopic(name=topic_name, num_partitions=3, replication_factor=1)
        admin.create_topics([topic])
        print(f"Topic {topic_name} created")
    except Exception as e:
        print(str(e))
        pass

    print("Reading parquet")
    df = pd.read_parquet("titanic_train_file_source.parquet").sort_values(by="dummy_timestamp")
    df["dummy_timestamp"] = datetime(2022, 1, 15, 2, 59, 50)
    iteration = 1

    cols_to_send = [
        "PassengerId",
        "Survived",
        "Pclass",
        "Name",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Ticket",
        "Fare",
        "Cabin",
        "Embarked",
        "dummy_timestamp",
    ]
    for row in df[cols_to_send].to_dict("records"):
        # Make event one more year recent to simulate fresher data
        row["dummy_timestamp"] = (row["dummy_timestamp"] + pd.Timedelta(weeks=52 + iteration)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        row["PassengerId"] += 1000
        producer.send(topic_name, json.dumps(row).encode())
        print(row)
        iteration += 1


if __name__ == "__main__":
    create_stream(TOPIC)
