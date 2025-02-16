import pandas as pd

# Load JSON file into a pandas DataFrame
df = pd.read_json("./image_data.json")  # Replace with your JSON file path

# Convert to Parquet format
df.to_parquet("./sample-files/image_data.parquet", engine="pyarrow")  # Saves as a Parquet file

print("JSON converted to Parquet successfully!")