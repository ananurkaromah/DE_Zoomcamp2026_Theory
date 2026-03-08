This post is part of a series where I document my learnings from the “Data Engineering Zoomcamp” course, created by DataTalksClub. The course material can be found on GitHub here: [DataTalksClub/data-engineering-zoomcamp: Free Data Engineering course!](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main)

# Data Ingestion Pipeline with dlt and BigQuery

This project demonstrates how to build a simple **data ingestion pipeline** using **Python**, **dlt (Data Load Tool)**, and **Google BigQuery**.

The pipeline extracts data from a public API, processes it with pagination, and loads the data into BigQuery.

The project is part of learning **Data Engineering concepts**, including:

- API data extraction
- Pagination handling
- Data pipeline creation
- Loading data into a data warehouse (BigQuery)

---

## Project Structure

```
.
├── extract_with_dlt.py
├── load_bigquery.py
├── test_api.py
└── README.md
```

---

## API Source

The data comes from the following public API:

```
https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
```

The API returns paginated data related to taxi rides used for data engineering practice.

---

## Files Explanation

### 1. test_api.py

This script tests the API using the `requests` library.

Purpose:

- Verify that the API is working
- Check pagination behavior
- Inspect the number of records per page

Key features:

- Sends GET requests to the API
- Iterates through pages
- Prints the number of records per page

Example output:

```
Page 1 loaded, records: 1000
Page 2 loaded, records: 1000
```

---

### 2. extract_with_dlt.py

This script demonstrates **data extraction using dlt with pagination**.

Key components:

- `RESTClient` for API requests
- `PageNumberPaginator` to handle pagination

Function:

```
paginated_getter()
```

Purpose:

- Connect to the API
- Iterate through paginated results
- Yield each page of data

The script prints the number of records from the first page as a quick test.

---

### 3. load_bigquery.py

This script builds a **complete data pipeline using dlt**.

Pipeline steps:

1. Extract data from the API
2. Use pagination to collect all records
3. Load the data into **Google BigQuery**

Resource definition:

```
@dlt.resource(name="rides", write_disposition="replace")
```

Pipeline configuration:

- Pipeline name: `taxi_data`
- Destination: `BigQuery`
- Dataset name: `taxi_rides`

Running the pipeline will automatically:

- Create the dataset (if it does not exist)
- Create tables
- Load the data

Example output:

```
Pipeline taxi_data completed successfully
Loaded rows into BigQuery dataset taxi_rides
```

---

## Requirements

Install the required Python packages:

```
pip install dlt requests
```

If you want to load data into BigQuery, you also need:

```
pip install dlt[bigquery]
```

---

## BigQuery Authentication

Before running the pipeline, authenticate with Google Cloud:

```
gcloud auth application-default login
```

Make sure your **Google Cloud project** has BigQuery enabled.

---

## How to Run

### 1. Test the API

```
python test_api.py
```

---

### 2. Test extraction with dlt

```
python extract_with_dlt.py
```

---

### 3. Run the pipeline and load data to BigQuery

```
python load_bigquery.py
```

---

## Technologies Used

- Python
- dlt (Data Load Tool)
- REST API
- Google BigQuery
- Requests library

---

## Learning Goals

This project helps practice:

- Building a simple **ETL/ELT pipeline**
- Handling **API pagination**
- Using **dlt for data ingestion**
- Loading data into a **cloud data warehouse**
- Structuring a **data engineering project**