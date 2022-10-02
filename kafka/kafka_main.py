import json
from datetime import datetime

import pandas as pd
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
import argparse
import os

BOOTSTRAP_SERVERS = [os.getenv("KAFKA_SERVER", "ERROR")]

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", default="setup", choices=["setup", "teardown"])

args = parser.parse_args()


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
    df = pd.read_parquet("titanic_train_file_source.parquet").sort_values(by="event_timestamp")
    df["event_timestamp"] = datetime(2022, 1, 15, 2, 59, 50)
    iteration = 1
    while True:
        for row in df[["PassengerId", "event_timestamp", "Pclass", "Fare"]].to_dict("records"):
            # Make event one more year recent to simulate fresher data
            row["event_timestamp"] = (row["event_timestamp"] + pd.Timedelta(weeks=52 + iteration)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            producer.send(topic_name, json.dumps(row).encode())
            print(row)
        iteration += 1


def teardown_stream(topic_name):
    try:
        admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
        print(admin.delete_topics([topic_name]))
        print(f"Topic {topic_name} deleted")
    except Exception as e:
        print(str(e))
        pass


if __name__ == "__main__":
    parsed_args = vars(args)
    mode = parsed_args["mode"]
    teardown_stream("drivers")
    if mode == "setup":
        create_stream("drivers")
