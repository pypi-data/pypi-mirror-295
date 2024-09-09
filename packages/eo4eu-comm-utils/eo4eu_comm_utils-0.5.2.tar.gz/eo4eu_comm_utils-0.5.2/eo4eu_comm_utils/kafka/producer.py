from logging import Logger
from confluent_kafka import Producer

from . import default_logger


class KafkaProducer:
    def __init__(self, topic: str, config: dict, logger: Logger = None):
        # self.topic = "system.dsl"
        self.topic = topic
        self.producer = Producer(config)
        if logger is None:
            logger = default_logger
        self.logger = logger

    def set_topic(self, topic: str):
        self.topic = topic

    def send_message(self, key: str, msg: str, topic: str = None):
        def _acked(err, msg):
            if err is not None:
                self.logger.error(f"Failed to deliver message: {str(msg)}: {str(err)}")
            else:
                self.logger.info(
                    f"Message produced: {str(msg.value())} on topic {self.topic}"
                )

        if topic is None:
            topic = self.topic

        self.producer.produce(topic, key=key, value=msg, callback=_acked)
        self.producer.flush()


class MockProducer:
    def __init__(self, topic: str = "", logger: Logger = None):
        self.topic = topic
        if logger is None:
            logger = default_logger
        self.logger = logger

    def set_topic(self, topic: str):
        self.topic = topic

    def send_message(self, key: str, msg: str, topic: str = None):
        if topic is None:
            topic = self.topic

        self.logger.info(f"Producer, key: {key}, topic: {topic}")
        self.logger.info(msg)
