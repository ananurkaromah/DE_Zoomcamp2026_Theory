import requests

BASE_API_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

page_number = 1

while True:
    params = {'page': page_number}
    response = requests.get(BASE_API_URL, params=params)
    page_data = response.json()

    if not page_data:
        print("No more data.")
        break

    print(f"Page {page_number} loaded, records: {len(page_data)}")

    page_number += 1

    if page_number > 2:  # limit test
        break
