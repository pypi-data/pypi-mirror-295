# data_quality_sdk/metrics_publisher.py
from kafka import KafkaProducer
import json

class MetricsPublisher:
    def __init__(self, kafka_broker):
        self.producer = KafkaProducer(bootstrap_servers=kafka_broker,
                                       value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def publish(self, topic, metrics):
        self.producer.send(topic, metrics)
        self.producer.flush()
