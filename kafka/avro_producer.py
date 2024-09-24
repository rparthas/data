from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField, StringSerializer

from User import User
from constants import read_config, TOPIC_USERS, SCHEMA_REGISTRY_URL, USER_SCHEMA_STR


def user_to_dict(user, ctx):
    return dict(name=user.name,
                favorite_number=user.favorite_number,
                favorite_color=user.favorite_color)


def create_users():
    users = [User("eabara", "123 Main St", 42, "green"),
             User("jsmith", "456 Elm St", 42, "blue"),
             User("sgarcia", "789 Oak St", 42, "red")]
    return users


def create_serializer():
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    return AvroSerializer(schema_registry_client,
                          USER_SCHEMA_STR,
                          user_to_dict)


def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))


if __name__ == '__main__':

    producer = Producer(read_config())
    avro_serializer = create_serializer()

    for user in create_users():
        producer.produce(TOPIC_USERS, key=StringSerializer('utf_8')(str(uuid4())),
                         value=avro_serializer(user, SerializationContext(TOPIC_USERS, MessageField.VALUE)),
                         callback=delivery_callback)

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()
