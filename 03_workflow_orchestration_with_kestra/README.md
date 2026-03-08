This post is part of a series where I document my learnings from the “Data Engineering Zoomcamp” course, created by DataTalksClub. The course material can be found on GitHub here: [DataTalksClub/data-engineering-zoomcamp: Free Data Engineering course!](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main)

# Kestra NYC Taxi Data Pipeline

This project demonstrates how to use **Kestra** to orchestrate a simple **data ingestion pipeline** for the NYC Taxi dataset.

The pipeline downloads taxi trip data from the **NYC TLC dataset**, processes it, and loads it into a **PostgreSQL database**.

Dataset source:

https://github.com/DataTalksClub/nyc-tlc-data/releases

- --

# Workflows

## 1. Hello World Workflow

A simple workflow to demonstrate basic Kestra concepts such as:

- Inputs
- Variables
- Logging
- Task execution
- Outputs
- Scheduling

The workflow prints a welcome message, generates an output, waits for a few seconds, and logs the result.

- --

## 2. Postgres Taxi Pipeline

This workflow ingests **NYC taxi trip data** into PostgreSQL.

Main steps:

1. Download taxi dataset (CSV)

2. Create database tables

3. Load data into a staging table

4. Generate a unique row ID

5. Merge new data into the final table

6. Clean temporary files

The pipeline supports two taxi types:

- `yellow`
- `green`
- --

## 3. Scheduled Taxi Pipeline

An automated version of the taxi pipeline that runs on a **monthly schedule**.

Schedules:

- Green taxi → 09:00 on the 1st day of each month
- Yellow taxi → 10:00 on the 1st day of each month

The workflow automatically determines the dataset based on the execution date.

- --

# Technologies Used

- Kestra (workflow orchestration)
- PostgreSQL
- Shell commands (wget, gunzip)
- NYC TLC Taxi Dataset
- --

# Learning Goal

This project demonstrates basic **data orchestration concepts**, including:

- workflow automation
- scheduled pipelines
- data ingestion
- staging tables
- incremental data loading