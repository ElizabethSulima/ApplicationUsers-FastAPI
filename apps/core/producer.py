import json

from kafka import KafkaProducer  # type:ignore[import-untyped]


producer = KafkaProducer(
    value_serializer=lambda value: json.dumps(value).encode()
)
