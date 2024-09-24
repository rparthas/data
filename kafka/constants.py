TOPIC_PURCHASES = 'purchases'
TOPIC_CUSTOMERS = 'customers'
TOPIC_USERS = 'users'
SCHEMA_REGISTRY_URL = 'http://localhost:8081'
USER_SCHEMA_STR = """
    {
        "namespace": "confluent.io.examples.serialization.avro",
        "name": "User",
        "type": "record",
        "fields": [
            {
                "name": "name",
                "type": "string"
            },
            {
                "name": "favorite_number",
                "type": "long"
            },
            {
                "name": "favorite_color",
                "type": "string"
            }
        ]
    }
    """


def read_config():
    # reads the client configuration from client.properties
    # and returns it as a key-value map
    config = {}
    with open("config.properties") as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                config[parameter] = value.strip()
    return config
