import json
from time import sleep

import pandas as pd
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic, ClusterMetadata
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--mode",
    default="setup",
    choices=["setup", "teardown"],
    help="Whether to setup or teardown a Kafka topic with driver stats events. Setup will teardown before beginning emitting events.",
)
parser.add_argument(
    "-b",
    "--bootstrap_servers",
    default="localhost:9092",
    help="Where the bootstrap server is",
)

args = parser.parse_args()

delivered_records = 0

# Optional per-message on_delivery handler (triggered by poll() or flush())
# when a message has been successfully delivered or
# permanently failed delivery (after retries).
def acked(err, msg):
    global delivered_records
    """Delivery report handler called on
    successful or failed delivery of message
    """
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        delivered_records += 1
        print("Produced record to topic {} partition [{}] @ offset {}"
            .format(msg.topic(), msg.partition(), msg.offset()))

def create_stream(topic_name, servers):
    topic_name = topic_name

    producer = None
    admin = None
    for i in range(30):
        try:
            producer = Producer({"bootstrap.servers": servers[0]})
            admin = AdminClient({"bootstrap.servers": servers[0]})
            print("SUCCESS: instantiated Kafka admin and producer")
            break
        except Exception as e:
            print(
                f"Trying to instantiate admin and producer with bootstrap servers {servers} with error {e}"
            )
            sleep(10)
            pass

    try:
        # Create Kafka input topic
        topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
        sleep(2)
        print(f"Topic {topic_name} created")
        out_topic = NewTopic("trip_processed_topic", num_partitions=1, replication_factor=1)
        admin.create_topics([out_topic])
        sleep(2)
        print(f"Topic trip_processed_topic created")
    except Exception as e:
        print(str(e))
        pass

    print("Reading Trip Data")
    df = pd.read_csv("input.csv", index_col=[0])
    print("Emitting events")
    iteration = 1
    df1 = df.drop(["key", "fare_amount"], axis=1)
    while True:
        for row in df1.to_dict("records"):
            producer.poll(0)
            producer.produce(topic_name, value=json.dumps(row), on_delivery=acked)
            # print(row)
            sleep(1.0)
        iteration += 1


def teardown_stream(topic_name, servers=["localhost:9092"]):
    try:
        admin = AdminClient({"bootstrap.servers": servers[0]})
        print(admin.delete_topics([topic_name]))
        sleep(2)
        print(f"Topic {topic_name} deleted")
        print(admin.delete_topics(["trip_processed_topic"]))
        sleep(2)
        print(f"Topic trip_processed_topic deleted")
    except Exception as e:
        print(str(e))
        pass


if __name__ == "__main__":
    parsed_args = vars(args)
    mode = parsed_args["mode"]
    servers = parsed_args["bootstrap_servers"]
    teardown_stream("trip_input_topic", [servers])
    if mode == "setup":
        create_stream("trip_input_topic", [servers])
