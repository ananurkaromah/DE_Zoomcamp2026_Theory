from dataclasses import dataclass
import json

@dataclass
class GreenTrip:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    total_amount: float
    lpep_pickup_datetime: str

def trip_from_row(row):
    return GreenTrip(
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        trip_distance=float(row['trip_distance']),
        total_amount=float(row['total_amount']),
        lpep_pickup_datetime=str(row['lpep_pickup_datetime'])
    )

def serializer(trip):
    return json.dumps(trip.__dict__).encode('utf-8')