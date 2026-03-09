## **Batch Processing with Apache Spark – Data Engineering Zoomcamp**

This repository contains my learning notes and exercises from the **Batch Processing with Apache Spark** module of the **Data Engineering Zoomcamp**. The course material can be found on GitHub here: [DataTalksClub/data-engineering-zoomcamp: Free Data Engineering course!](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main)

The goal of this module is to understand how large-scale data processing works using **Apache Spark** and **PySpark**, and how Spark fits into modern **data lake architectures**.

---

### **What is Apache Spark?**

Apache Spark is an **open-source distributed computing engine** designed for large-scale data processing.

Spark allows data engineers to process **massive datasets efficiently** by distributing computation across multiple nodes.

Key capabilities:

- Distributed data processing
- In-memory computation
- Batch and streaming processing
- Integration with machine learning pipelines
- Multi-language support (Scala, Python, Java, R)

In this module we use **PySpark** to interact with Spark using Python.

---

### **When to Use Spark**

Spark is typically used when working with data stored in **data lakes**, such as:

- Amazon S3
- Google Cloud Storage

These storage systems often contain files such as:

- Parquet
- CSV
- JSON

Typical pipeline:

```
Raw Data
↓
Data Lake
↓
Spark Processing
↓
Processed Data
↓
Data Warehouse / ML
```

Spark is especially useful when:

- SQL alone is not sufficient
- complex transformations are required
- machine learning pipelines are needed
- datasets are too large for single-machine processing

---

### **Learning Objectives**

In this module I practiced:

- Installing Spark locally
- Running PySpark
- Creating Spark Sessions
- Working with Spark DataFrames
- Creating transformations
- Using UDFs (User Defined Functions)
- Aggregations with Spark
- Understanding Spark execution

---

### **Environment Setup**

This setup was tested on:

- Ubuntu (WSL)
- VSCode
- Python environment managed with `uv`

---

### **Install Java**

Spark requires Java.

```
sudo apt update
sudo apt install default-jdk
```

Verify installation:

```
java --version
```

---

### **Install PySpark**

Using `uv`:

```
uv init
uv add pyspark
```

Or using pip:

```
pip install pyspark
```

---

### **Running Spark**

Create a simple Spark test script:

```
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("spark-test") \
    .getOrCreate()

df = spark.range(10)

df.show()

spark.stop()
```

Run:

```
uv run python test_spark.py
```

---

### **Understanding SparkSession**

SparkSession is the **entry point to Spark**.

```
SparkSession.builder
```

| **Parameter** | **Purpose** |
| --- | --- |
| master("local[*]") | Run Spark locally using all CPU cores |
| appName() | Name of the Spark application |
| getOrCreate() | Create or reuse an existing session |

---

### **Spark Data Processing Example**

Example transformation:

```
df_trips \
.withColumn(
    "duration_hours",
    duration_udf(
        df_trips.tpep_pickup_datetime,
        df_trips.tpep_dropoff_datetime
    )
) \
.groupBy() \
.max("duration_hours") \
.show()
```

Pipeline flow:

```
Raw Taxi Data
↓
Add duration column
↓
Aggregation
↓
Find longest trip
```

---

### **Spark UI**

When running Spark locally, you can access:

```
http://localhost:4040
```

Spark UI helps monitor:

- Jobs
- Stages
- Executors
- Task execution

---

### **Spark vs SQL Engines**

Tools like:

- Hive
- Presto
- Athena allow querying files in data lakes using SQL.

However Spark is preferred when:

- transformations are complex
- custom logic is required
- Python workflows are needed
- machine learning pipelines are involved

---

### **Homework Solution**

The full solution for the Batch Processing Homework can be found here:

https://github.com/ananurkaromah/data-engineering-zoomcamp2026-homework/blob/main/Homework/06-batch/homework-batch-spark.md

---

### **Key Takeaways**

- Spark enables distributed big data processing
- PySpark allows Python users to work with Spark
- Spark is widely used in modern data engineering pipelines
- DataFrames are the main abstraction in Spark
- Spark can scale from local environments to large clusters

---

### **References**

Apache Spark documentation https://spark.apache.org/docs/latest/
Data Engineering Zoomcamp https://github.com/DataTalksClub/data-engineering-zoomcamp