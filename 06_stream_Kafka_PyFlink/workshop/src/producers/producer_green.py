import pandas as pd
from kafka import KafkaProducer
import time
from src.models import trip_from_row, serializer

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"

df = pd.read_parquet(url).head(1000)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=serializer
)

topic = "green-trips"

# START TIMER
t0 = time.time()

for _, row in df.iterrows():
    trip = trip_from_row(row)
    producer.send(topic, value=trip)
    time.sleep(0.01)  # simulate streaming

producer.flush()

# END TIMER
t1 = time.time()

print(f"\n Total time: {t1 - t0:.2f} seconds")