from confluent_kafka import TopicCollection
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewPartitions

from constants import read_config


def get_topic_metadata():
    global topic
    metadata = admin_client.list_topics(timeout=10)
    for topic in metadata.topics:
        topic_result = admin_client.describe_topics(TopicCollection([topic]))
        topic_description = topic_result[topic].result()
        print(f"Topic Name: {topic_description.name}")
        print(f"Topic Id: {topic_description.topic_id}")
        print(f"Topic Partitions size: {len(topic_description.partitions)}")
        for partition in topic_description.partitions:
            print(f"Topic Partition leader {partition.leader.id} for {partition.id}")
        print("##################")


if __name__ == '__main__':
    admin_client = AdminClient(read_config())
    new_partition = NewPartitions("users", new_total_count=3)
    admin_client.create_partitions([new_partition])
    get_topic_metadata()
