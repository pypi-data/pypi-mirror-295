from aiokafka import AIOKafkaProducer
import pytest
import random
import string
import json
import time
from scidx.client import sciDXClient

# Constants
API_URL = "http://localhost:8000"
KAFKA_HOST = '155.101.6.194'
KAFKA_PORT = '9092'
KAFKA_TOPIC_PREFIX = 'random_topic_example_'
OWNER_ORG = "test_org"
USERNAME = "placeholder@placeholder.com"
PASSWORD = "placeholder"

def generate_unique_kafka_topic():
    return KAFKA_TOPIC_PREFIX + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# class KafkaProducer:
#     def __init__(self, host, port, topic):
#         self.host = host
#         self.port = port
#         self.topic = topic

#     async def send_incremental_messages(self, start_value: int, end_value: int, step: int = 1):
#         producer = AIOKafkaProducer(bootstrap_servers=f"{self.host}:{self.port}")
#         await producer.start()
#         try:
#             for i in range(start_value, end_value, step):
#                 message = {"x_field": i, "y": f"message_{i}"}
#                 await producer.send_and_wait(self.topic, json.dumps(message).encode('utf-8'))
#                 print(f"Sent message {i}: {message}")
#         finally:
#             await producer.stop()

@pytest.fixture
def kafka_client():
    client = sciDXClient(API_URL)
    client.login(USERNAME, PASSWORD)
    return client

@pytest.mark.asyncio
async def test_kafka_stream_processing(kafka_client):
    kafka_topic = generate_unique_kafka_topic()

    # producer = KafkaProducer(KAFKA_HOST, KAFKA_PORT, kafka_topic)
    # await producer.send_incremental_messages(start_value=1, end_value=151, step=1)

    dataset_data = {
        "dataset_name": kafka_topic,
        "dataset_title": "Incremental Values Example",
        "owner_org": OWNER_ORG,
        "kafka_topic": 'CSCI',
        "kafka_host": KAFKA_HOST,
        "kafka_port": KAFKA_PORT,
        "dataset_description": "This dataset contains incremental values from 1 to 150.",
        "extras": {
            "key1": "value1",
            "key2": "value2"
        },
        "mapping": {
            "x_field": "x",
            "y": "y"
        }
    }
    kafka_client.register_kafka(**dataset_data)

    time.sleep(2)

    stream_response = kafka_client.create_kafka_stream([kafka_topic], ["x_field>=0", "y>0"])
    print(stream_response)

    stream_topic = stream_response.get("topic")
    assert stream_topic is not None, "Failed to create Kafka stream"

    print(f"Waiting for stream topic: {stream_topic} to be available...")
    # time.sleep(10)

    # # Timeout mechanism to ensure the test doesn't hang
    # timeout_seconds = 30
    # start_time = time.time()
    # consumed_messages = []

    # while True:
    #     messages = kafka_client.consume_kafka_messages(topic=stream_topic)
    #     consumed_messages.extend(messages)

    #     if len(consumed_messages) >= 100 or (time.time() - start_time) > timeout_seconds:
    #         break

    #     time.sleep(1)  # Short sleep to avoid overwhelming the API

    # assert len(consumed_messages) == 100, f"Expected 100 messages, but received {len(consumed_messages)}"
    # for message in consumed_messages:
    #     data = json.loads(message)
    #     value = data.get("x_field")
    #     assert 1 <= value < 101, f"Unexpected value {value} in message {message}"

    # print(f"Messages from stream topic {stream_topic}:\n")
    # for message in consumed_messages:
    #     print(message)

if __name__ == "__main__":
    pytest.main([__file__])
