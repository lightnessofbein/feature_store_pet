import json
import requests
import config
import time
from kafka import KafkaConsumer
from collections import defaultdict


def send_batch(items):
    push_info = {
        "push_source_name": config.PUSH_SOURCE_NAME,
        "df": items,
        "to": "online",
    }
    response = requests.post(f"http://{config.PUSH_SERVER_URL}/push", data=json.dumps(push_info))
    return response.status_code


def merge_messages(batch_dict, message):
    for k in message.keys():
        batch_dict[k].append(message[k])
    return batch_dict


consumer = KafkaConsumer(
    config.KAFKA_TOPIC,
    bootstrap_servers=config.BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="titanic-4",
    max_poll_records=32,
    value_deserializer=lambda m: json.loads(m),
)


if __name__ == "__main__":
    print("aaa")
    counter = 0
    starttime = time.time()
    batch_dict = defaultdict(list)

    for message in consumer:
        print("hmm")
        batch_dict = merge_messages(batch_dict, message.value)
        counter += 1
        time_diff = time.time() - starttime
        print(batch_dict)
        if counter == config.BATCH_SIZE or time_diff > config.TIMEOUT:
            response = send_batch(batch_dict)
            batch_dict = defaultdict(list)
            counter = 0
            starttime = time.time()
            print(response)
