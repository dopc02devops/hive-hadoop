from hdfs import InsecureClient
import pandas as pd
import numpy as np
from hdfs.util import HdfsError
from faker import Faker
import os

# HDFS Connection - Update with the correct URL
HDFS_NAMENODE_URL = "http://namenode:9870"  # Update this if necessary, to match your Docker or host setup
HDFS_USER = "transaction"  # Make sure this user exists on HDFS or change it to the correct user

# Connect to HDFS
try:
    client = InsecureClient(HDFS_NAMENODE_URL, user=HDFS_USER)
    print("Successfully connected to HDFS.")
except Exception as e:
    print(f"Error connecting to HDFS: {e}")
    exit(1)

# Ensure the HDFS directory exists
hdfs_directory = "/user/transaction"

# Check if the directory exists, and create it if it doesn't
try:
    if not client.status(hdfs_directory, strict=False):
        print(f"Directory {hdfs_directory} does not exist. Creating it...")
        client.makedirs(hdfs_directory)
    else:
        print(f"Directory {hdfs_directory} already exists.")
except HdfsError as e:
    print(f"Error checking HDFS directory: {e}")
    exit(1)

# Initialize Faker to generate realistic names and addresses
fake = Faker()

# Generate sample bank transaction data with 3000 rows
try:
    transaction_data = {
        "transaction_id": np.arange(1, 3001),
        "user_id": np.random.randint(1, 501, 3000),  # Random user IDs between 1 and 500
        "name": [fake.name() for _ in range(3000)],  # Generate random names
        "address": [fake.address().replace("\n", " ") for _ in range(3000)],  # Generate random addresses
        "age": np.random.randint(20, 80, 3000),  # Random ages between 20 and 80
        "transaction_date": pd.to_datetime(np.random.choice(pd.date_range("2024-01-01", "2024-12-31", freq="h"), 3000)),
        
        # Dynamic transaction types (weighted probabilities for more realistic distribution)
        "transaction_type": np.random.choice(
            ["Deposit", "Withdrawal", "Transfer", "Loan Repayment", "Interest Credit"],
            3000, 
            p=[0.3, 0.4, 0.2, 0.05, 0.05]
        ),
        "amount": np.random.uniform(10, 5000, 3000),  # Random transaction amounts between 10 and 5000
        "balance_after": np.random.uniform(1000, 100000, 3000),  # Random balance after transaction
    }

    df_transactions = pd.DataFrame(transaction_data)
    print(f"Successfully generated {len(df_transactions)} transactions.")
except Exception as e:
    print(f"Error generating transaction data: {e}")
    exit(1)

# Save locally
try:
    df_transactions.to_csv("transactions.csv", index=False)
    df_transactions.to_json("transactions.json", orient="records", lines=True)
    df_transactions.to_parquet("transactions.parquet", engine="pyarrow")
    print("Transaction files generated locally.")
except Exception as e:
    print(f"Error saving local files: {e}")
    exit(1)

# Check if the file exists on HDFS and remove if needed, then upload
hdfs_file_path_csv = hdfs_directory + "/transactions.csv"
hdfs_file_path_json = hdfs_directory + "/transactions.json"
hdfs_file_path_parquet = hdfs_directory + "/transactions.parquet"

# Check and delete existing files (if any)
for file_path in [hdfs_file_path_csv, hdfs_file_path_json, hdfs_file_path_parquet]:
    try:
        if client.status(file_path, strict=False):  # Check if file exists
            print(f"File {file_path} already exists. Deleting it...")
            client.delete(file_path)  # Delete the existing file
    except HdfsError:
        print(f"File {file_path} does not exist, safe to upload.")

# Upload files to HDFS
try:
    client.upload(hdfs_file_path_csv, "transactions.csv", overwrite=True)
    client.upload(hdfs_file_path_json, "transactions.json", overwrite=True)
    client.upload(hdfs_file_path_parquet, "transactions.parquet", overwrite=True)
    print("Transaction files uploaded to HDFS successfully.")
except Exception as e:
    print(f"Error uploading files to HDFS: {e}")
    exit(1)

# List files in the directory
try:
    uploaded_files = client.list(hdfs_directory)
    print("\nFiles in HDFS directory:")
    for file in uploaded_files:
        print(file)
except Exception as e:
    print(f"Error listing files in HDFS directory: {e}")
    exit(1)
