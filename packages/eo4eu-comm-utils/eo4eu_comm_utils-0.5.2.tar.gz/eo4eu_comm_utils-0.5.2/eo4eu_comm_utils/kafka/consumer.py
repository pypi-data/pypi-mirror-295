import time
from typing import List
from logging import Logger
from confluent_kafka import Consumer

from . import default_logger


class KafkaConsumer:
    def __init__(self, topics: List[str], config: dict, handler, logger: Logger = None):
        self.consumer = Consumer(config)
        self.topics = topics
        self.handler = handler
        if logger is None:
            logger = default_logger
        self.logger = logger

    def consume(self):
        try:
            self.consumer.subscribe(self.topics)
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None or msg.error():
                    continue

                decoded_msg = msg.value().decode("utf-8")
                self.logger.info(
                    f"New message received: {decoded_msg} from topic {msg.topic()}"
                )
                self.handler(decoded_msg)
        finally:
            self.consumer.close()


class MockConsumer:
    def __init__(self, wait_time, runs, handler, message = ""):
        self.message = message
        self.wait_time = wait_time
        self.runs = runs
        self.handler = handler

    def consume(self):
        for _ in range(self.runs):
            self.handler(self.message)
            time.sleep(self.wait_time)
