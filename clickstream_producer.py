from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

pages = ['home', 'search', 'product', 'cart', 'checkout']
users = ['user1', 'user2', 'user3', 'user4']

while True:
    event = {
        'user': random.choice(users),
        'page': random.choice(pages),
        'timestamp': int(time.time())
    }
    producer.send('clickstream', event)
    print(f"Sent: {event}")
    time.sleep(1)  # send one event per second
