# data-lakes


##########################
Data Storage & Processing
##########################
Databases:
    - Relational: PostgreSQL, MySQL
    - NoSQL: MongoDB, Cassandra
    - Data Warehouses: Snowflake, BigQuery, Redshift
    - Big Data Processing:
    - Apache Spark (PySpark)
    - Apache Kafka (streaming)
    - Hadoop (optional but good to know)


AWS: S3, Glue, Redshift, Athena, Lambda
GCP: BigQuery, Dataflow
Azure: Synapse, Data Factory


1. Data Storage & Databases
Relational Databases: PostgreSQL, MySQL (for structured data)
NoSQL Databases: MongoDB, Cassandra, Redis (you’re already learning MongoDB & Cassandra)
Data Lakes: Apache Iceberg, Delta Lake
2. Data Processing & Pipelines
ETL Tools: Apache NiFi, Airflow, dbt
Streaming Data: Apache Kafka, Pulsar, Flink
Big Data Processing: Apache Spark, Dask
3. Cloud & Infrastructure for Data
AWS: S3, Glue, Redshift, Athena, EMR
Azure: Data Factory, Synapse Analytics
GCP: BigQuery, Dataflow








1. Data Lakes & Warehouses
Apache Hadoop (HDFS) – Used for large-scale distributed storage, often paired with Spark.
Amazon S3 – Scalable object storage, widely used for AI workloads in the cloud.
Google BigQuery / Snowflake – Cloud data warehouses optimised for analytics.
Delta Lake (Databricks) – Enhances data lakes with ACID transactions.
2. NoSQL Databases
MongoDB – Common for semi-structured data (JSON) in AI applications.
Cassandra – Used when scalability and high availability are required.
Redis – Fast in-memory database, great for caching and real-time ML inference.
3. Relational Databases (SQL-based)
PostgreSQL – Popular for structured AI data storage, supports JSON and extensions like TimescaleDB.
MySQL – Used in AI applications but less common for large-scale analytics.
4. Vector Databases (For AI Search & Embeddings)
FAISS (Facebook AI Similarity Search) – Used for fast nearest-neighbour search in high-dimensional spaces.
Milvus – Open-source vector database optimised for large-scale AI applications.
Pinecone / Weaviate – Managed vector search services.
5. Distributed & Cloud-Native Storage
Google Cloud Storage / AWS S3 / Azure Blob Storage – Used for AI model training pipelines.
Ceph – Distributed object storage for on-prem AI workloads.
For your DevOps & Data Engineering focus, you might want to explore MongoDB, Cassandra, and S3 for AI workloads. Let me know if you want help setting up any of these in Docker Compose! 




clear cache: docker system prune -a
docker-compose up --build -d



python3 -m venv venv
source venv/bin/activate
deactivate
