from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer('dbserver1.inventory.products',
                         group_id='my-group',
                         bootstrap_servers=['kafka:9092'],
                         auto_offset_reset='earliest')

for message in consumer:
    print(message.value.decode('utf-8'))
