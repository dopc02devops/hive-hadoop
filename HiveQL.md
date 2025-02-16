# HIVEQL

#####
```sh
docker-compose up --build -d
```

## Generate Data with `hdfs_data_copy.sh`
```sh
chmod +x hdfs_data_copy.sh
./python-scripts/hdfs_data_copy.sh <user_name> <container_id>
```

## Convert JSON to Hive-JSON Data
```sh
python3 ./python-scripts/hive-json-convert.py
```

## Convert JSON to Hive-Parquet Data
```sh
python3 ./python-scripts/hive-parquet-conver.py
parquet-tools cat sample-files/image_data.parquet
```

## Determine Data Format
1. Login to HDFS server or container (namenode):
```sh
docker exec -it <container_id> /bin/bash
```
2. Check file content:
```sh
hdfs dfs -cat /user/Goli/sample-files/sample.csv | head -n 10
hdfs dfs -cat /user/tweeter/tweets.csv | head -n 10
hdfs dfs -cat /user/transaction/transactions.csv | head -n 10
hdfs dfs -cat /user/image_user/sample-files/image_data.json | head -n 10
```

## Create Tables
### JSON Data Table
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS json_data (
    image_id INT,
    image_name STRING,
    image_url STRING,
    image_type STRING,
    image_data STRING
)
COMMENT 'Table containing image data'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/imager/sample-files/'
TBLPROPERTIES ('created_by'='imager', 'format_version'='v1');
```

### Transactions Table
```sql
CREATE EXTERNAL TABLE transactions_table (
    transaction_id INT,
    user_id INT,
    name STRING,
    address STRING,
    age INT,
    transaction_date TIMESTAMP,
    transaction_type STRING,
    amount DOUBLE,
    balance_after DOUBLE
)
COMMENT 'Table containing transactions data'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/transaction/'
TBLPROPERTIES ('created_by'='transaction', 'format_version'='v1');
```

## Insert Metadata into Hive
```sql
LOAD DATA INPATH '/user/transaction/transactions.csv' INTO TABLE transactions_table;
LOAD DATA INPATH '/user/imager/sample-files/image_data.json' INTO TABLE json_data;
```

## HiveQL Queries
### Basic Queries
```sql
SELECT * FROM json_data LIMIT 10;
SELECT * FROM transactions_table LIMIT 10;
```

### Aggregations and Calculations
```sql
SELECT SUM(amount) AS total_deposit
FROM transactions_table
WHERE transaction_type = 'Deposit';
```

```sql
SELECT
    SUM(CASE WHEN transaction_type = 'Deposit' THEN amount ELSE 0 END) * 100.0 / SUM(amount) AS deposit_percentage
FROM transactions_table;
```

```sql
SELECT
    transaction_type,
    SUM(amount) AS total_amount,
    (SUM(amount) * 100.0) / (SELECT SUM(amount) FROM transactions_table) AS percentage
FROM transactions_table
GROUP BY transaction_type;
```

### Monthly Deposit Growth Rate
```sql
WITH MonthlyDeposits AS (
    SELECT
        DATE_TRUNC('month', transaction_date) AS month,
        SUM(CASE WHEN transaction_type = 'Deposit' THEN amount ELSE 0 END) AS total_deposit
    FROM transactions_table
    GROUP BY DATE_TRUNC('month', transaction_date)
)
SELECT
    month,
    total_deposit,
    LAG(total_deposit) OVER (ORDER BY month) AS previous_month_deposit,
    (total_deposit - LAG(total_deposit) OVER (ORDER BY month)) * 100.0 / NULLIF(LAG(total_deposit) OVER (ORDER BY month), 0) AS growth_rate_percentage
FROM MonthlyDeposits;
```

### User-Based Aggregations
```sql
SELECT
    user_id,
    SUM(amount) AS total_deposit,
    (SUM(amount) * 100.0) / (SELECT SUM(amount) FROM transactions_table WHERE transaction_type = 'Deposit') AS contribution_percentage
FROM transactions_table
WHERE transaction_type = 'Deposit'
GROUP BY user_id
ORDER BY contribution_percentage DESC;
```

### Transaction-Based Queries
```sql
SELECT transaction_date,
    SUM(amount) OVER (ORDER BY transaction_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM transactions_table
WHERE transaction_type = 'Deposit';
```

```sql
SELECT user_id,
    transaction_id,
    amount,
    RANK() OVER (PARTITION BY user_id ORDER BY amount DESC) AS rank
FROM transactions
WHERE transaction_type = 'Deposit';
```

### Filtering and Grouping
```sql
SELECT transaction_id, user_id, transaction_date, amount
FROM transactions
WHERE transaction_date > DATE_SUB(CURRENT_DATE, 30);
```

```sql
SELECT user_id,
    COUNT(CASE WHEN transaction_type = 'Deposit' THEN 1 END) AS deposit_count,
    COUNT(CASE WHEN transaction_type = 'Withdrawal' THEN 1 END) AS withdrawal_count
FROM transactions
GROUP BY user_id;
```

```sql
SELECT user_id,
    SUM(amount) AS total_deposit,
    AVG(balance_after) AS avg_balance_after
FROM transactions
WHERE transaction_type = 'Deposit'
GROUP BY user_id
HAVING total_deposit > 10000 AND avg_balance_after > 20000;
```

### Union Queries
```sql
SELECT transaction_id, user_id, amount, 'Deposit' AS transaction_type
FROM transactions
WHERE transaction_type = 'Deposit'
UNION ALL
SELECT transaction_id, user_id, amount, 'Withdrawal' AS transaction_type
FROM transactions
WHERE transaction_type = 'Withdrawal';
```

### Yearly and Monthly Aggregations
```sql
SELECT YEAR(transaction_date) AS year,
       MONTH(transaction_date) AS month,
       SUM(amount) AS total_deposit
FROM transactions
WHERE transaction_type = 'Deposit'
GROUP BY YEAR(transaction_date), MONTH(transaction_date)
ORDER BY year, month;
```

### Top Transactions
```sql
SELECT transaction_id, user_id, amount
FROM transactions
WHERE transaction_type = 'Deposit'
ORDER BY amount DESC
LIMIT 5;
```

## Drop Tables
```sql
DROP TABLE image_data;
DROP TABLE transactions_table;
```

