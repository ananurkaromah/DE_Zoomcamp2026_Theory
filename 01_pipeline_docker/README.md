
This post is part of a series where I document my learnings from the “Data Engineering Zoomcamp” course, created by DataTalksClub. The course material can be found on GitHub here: [DataTalksClub/data-engineering-zoomcamp: Free Data Engineering course!](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main)


# Dockerized Data Ingestion Pipeline (PostgreSQL + Python)

This repository demonstrates how to build a **Docker-based data ingestion pipeline** using **PostgreSQL**, **Python**, and **Docker Compose**.

The project is designed as a **Data Engineering portfolio project**, focusing on containerization, service networking, and reproducible environments.


---

## Project Overview

### Docker Setup

1. **Use Docker networking for inter-container communication**
    
    ```jsx
    docker network create pg-network
    ```
    
2. **PostgreSQL container**
    
    Run the following Docker command to start a PostgreSQL container:
    
    ```jsx
       docker run -it \
    	-e POSTGRES_USER="root" \
    	-e POSTGRES_PASSWORD="root" \
    	-e POSTGRES_DB="ny_taxi" \
    	-v ../ny_taxi_postgres_data:/var/lib/postgresql \
    	-p 5432:5432 \
    	--network=pg-network \
    	--name pgdatabase \
    	postgres:18
    ```
    
3. **pgAdmin Container**
    
    Launch a pgAdmin container with the following command:
    
    ```jsx
    docker run -it \
      -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
      -e PGADMIN_DEFAULT_PASSWORD="root" \
      -v pgadmin_data:/var/lib/pgadmin \
      -p 8085:80 \
      --network=pg-network \
      --name pgadmin \
      dpage/pgadmin4
    ```
<br>
<br>

### Data Pipeline

**Building Docker Image**

Build a Docker image for the data ingestion pipeline:

```jsx
docker build -t taxi_ingest:v001 .
```

**Running Data Pipeline Container**

Run the data ingestion pipeline container:

**container yellow taxi 2021_1**

```jsx
docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
  --year=2021 \
  --month=1 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_1 \
  --chunksize=100000
 
```

**container green taxi_2025_11**

```jsx
docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
  --year=2025 \
  --month=11 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --data-type=green \
  --target-table=green_taxi
```

**container taxi zone**

```jsx

docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --data-type=zone \
  --target-table=taxi_zone
```

For ingestion data using docker_compose.yaml  just settle the network

network will replace with the  *--network=01_pipeline_docker_default \**
<br>
<br>

### Orchestrate services using Docker Compose

Docker Compose is used to orchestrate multiple containers. It provides a way to define and run multi-container Docker applications. In this project, it is used to define and run the entire stack in a more organized manner.

To deploy the entire stack using Docker Compose:

```
docker-compose up
```

In detached mode:

```
docker-compose up -d
```

To stop the containers:

```
docker-compose down
```
