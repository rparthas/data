from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

from constants import read_config, TOPIC_USERS, SCHEMA_REGISTRY_URL, USER_SCHEMA_STR
from User import User


def dict_to_user(obj, ctx):
    return User(name=obj['name'],
                address=None,
                favorite_number=obj['favorite_number'],
                favorite_color=obj['favorite_color'])


if __name__ == '__main__':
    consumer_conf = read_config()
    consumer_conf.update({
        'group.id': 'user_consumer_group',
        'auto.offset.reset': 'earliest'
    })

    consumer = Consumer(consumer_conf)

    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    avro_deserializer = AvroDeserializer(schema_registry_client,
                                         schema_str=USER_SCHEMA_STR,
                                         from_dict=dict_to_user)

    consumer.subscribe([TOPIC_USERS])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            user = avro_deserializer(msg.value(), SerializationContext(TOPIC_USERS, MessageField.VALUE))
            print(f"""Consumed event from topic {msg.topic()}: 
                    key = {msg.key().decode('utf-8')}, value = {user.name}, {user.favorite_number}, {user.favorite_color}""")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
