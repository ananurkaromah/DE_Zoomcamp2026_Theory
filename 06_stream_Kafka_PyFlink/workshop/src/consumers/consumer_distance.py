from kafka import KafkaConsumer
import json

server = 'localhost:9092'
topic = 'green-trips'

def deserializer(data):
    return json.loads(data.decode('utf-8'))

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='q3-consumer',
    value_deserializer=deserializer
)

count = 0

print("Listening...")

for message in consumer:
    trip = message.value
    
    if trip['trip_distance'] > 5:
        count += 1

    # stop setelah 1000 data (biar tidak infinite loop)
    if count >= 1000:
        break

print(f"\nTrips with distance > 5: {count}")

consumer.close()