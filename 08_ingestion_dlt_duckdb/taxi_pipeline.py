import dlt
import requests

BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

# Extract data dari API (paginated)
@dlt.resource(name="taxi_trips")
def taxi_data():
    page = 1

    while True:
        response = requests.get(f"{BASE_URL}?page={page}")
        data = response.json()

        # Stop kalau halaman kosong
        if not data:
            break

        for record in data:
            yield record

        print(f"Loaded page {page}")
        page += 1


# Buat pipeline
pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="nyc_taxi"
)

# Run pipeline
load_info = pipeline.run(taxi_data())

print(load_info)