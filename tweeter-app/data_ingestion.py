from hdfs import InsecureClient
import tweepy
import pandas as pd
import numpy as np
from hdfs.util import HdfsError
import os
import time  # To handle rate limit pauses

# HDFS Connection - Update with the correct URL
HDFS_NAMENODE_URL = "http://namenode:9870"  # Update this if necessary
HDFS_USER = "tweeter"  # Make sure this user exists on HDFS or change it to the correct user

# Twitter API credentials - Update these with your own
API_KEY = "wFcpzLd7AKNHk72A3xjaP8Z2u"
API_SECRET_KEY = "qO3w4f6xFzzx2o00DtF6LU64W9mdugSaymqb6XUmwFRej3e5uD"
ACCESS_TOKEN = "1887574269607223298-QoXGZs4wUkEYnfpKLAelt6rMv16RtT"
ACCESS_TOKEN_SECRET = "5RX3VQoWiHV6D4l1d9knWHAmufpQYQTOP9hYTFjeqoswC"

# Connect to HDFS
try:
    client = InsecureClient(HDFS_NAMENODE_URL, user=HDFS_USER)
    print("Successfully connected to HDFS.")
except Exception as e:
    print(f"Error connecting to HDFS: {e}")
    exit(1)

# Ensure that the user directory exists (if necessary)
hdfs_user_directory = f"/user/{HDFS_USER}"

try:
    # Check if the user's HDFS directory exists
    client.status(hdfs_user_directory)
    print(f"HDFS directory for user {HDFS_USER} already exists.")
except HdfsError:
    print(f"HDFS directory for user {HDFS_USER} does not exist. Creating...")
    client.makedirs(hdfs_user_directory)  # Create the directory if it doesn't exist
    print(f"Created HDFS directory for user {HDFS_USER}.")

# Twitter API authentication
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# List of famous Twitter users to get tweets from
famous_people = [
    "BarackObama", "elonmusk", "katyperry", "justinbieber", "rihanna",
    "taylorswift13", "Cristiano", "ladygaga", "KimKardashian", "britneyspears",
    "billgates", "oprah", "jimmyfallon", "selenagomez", "shakira"
]

# Fetch tweets from famous people
tweets_data = []

for user in famous_people:
    try:
        print(f"Fetching tweets for {user}...")
        tweets = api.user_timeline(screen_name=user, count=100, tweet_mode="extended")  # Get 100 latest tweets
        for tweet in tweets:
            tweets_data.append({
                "user": user,
                "tweet_id": tweet.id,
                "created_at": tweet.created_at,
                "tweet": tweet.full_text,
                "retweets": tweet.retweet_count,
                "likes": tweet.favorite_count,
            })
        print(f"Successfully fetched tweets for {user}.")
    except tweepy.errors.Forbidden as e:
        print(f"Forbidden error for {user}: {e}")
        continue  # Skip this user if the endpoint is not accessible
    except tweepy.TweepyException as e:  # General exception handling for Tweepy
        print(f"Error fetching tweets for {user}: {e}")
        continue

# Convert tweet data into a pandas DataFrame
try:
    df_tweets = pd.DataFrame(tweets_data)
    print(f"Successfully generated {len(df_tweets)} tweets.")
except Exception as e:
    print(f"Error generating tweet data: {e}")
    exit(1)

# Save locally
try:
    df_tweets.to_csv("tweets.csv", index=False)
    df_tweets.to_json("tweets.json", orient="records", lines=True)
    df_tweets.to_parquet("tweets.parquet", engine="pyarrow")
    print("Tweet files generated locally.")
except Exception as e:
    print(f"Error saving local files: {e}")
    exit(1)

# Check if the file exists on HDFS and remove if needed, then upload
hdfs_directory = "/user/tweeter"
hdfs_file_path_csv = hdfs_directory + "/tweets.csv"
hdfs_file_path_json = hdfs_directory + "/tweets.json"
hdfs_file_path_parquet = hdfs_directory + "/tweets.parquet"

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
    client.upload(hdfs_file_path_csv, "tweets.csv", overwrite=True)
    client.upload(hdfs_file_path_json, "tweets.json", overwrite=True)
    client.upload(hdfs_file_path_parquet, "tweets.parquet", overwrite=True)
    print("Tweet files uploaded to HDFS successfully.")
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
