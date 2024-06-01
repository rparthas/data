from confluent_kafka import Consumer, KafkaError

from kafka.constants import TOPIC_PURCHASES

conf = {
    'bootstrap.servers': 'localhost:39092',
    'auto.offset.reset': 'earliest',
    'group.id': 'purchases-consumer-group',
}

c = Consumer(conf)
c.subscribe([TOPIC_PURCHASES])

try:
    while True:
        msgs = c.consume(num_messages=10, timeout=1.0)
        for msg in msgs:
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            print('Received message: {} from {}'.format(msg.value().decode('utf-8'),
                                                        msg.key().decode('utf-8')))

finally:
    c.close()
