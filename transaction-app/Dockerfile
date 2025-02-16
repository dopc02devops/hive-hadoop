# Use Python 3.9 as the base image
FROM python:3.9

# Install cron and other dependencies
RUN apt-get update && apt-get install -y cron && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script and cron job
COPY data_ingestion.py .

# Make the Python script executable
RUN chmod +x data_ingestion.py

# Add the cron job
RUN echo "*/3 * * * * root /usr/local/bin/python3 /app/data_ingestion.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/crontab

# Set correct permissions for the crontab
RUN chmod 644 /etc/cron.d/crontab

# Start cron service in the foreground
ENTRYPOINT ["cron", "-f"]
