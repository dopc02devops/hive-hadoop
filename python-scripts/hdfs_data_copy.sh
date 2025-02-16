#!/bin/bash

# Function to check if the last command was successful
check_error() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

# Check if the correct number of arguments are passed
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <container_id>"
    exit 1
fi

# Get parameters
username=$1
container_id=$2

# 1. Copy files to HDFS Docker container
echo "Copying files to container..."
docker cp ./sample-files $container_id:/home/
check_error "Failed to copy files to container."

# Check if files are in /home/sample-files
echo "Checking if /home/sample-files exists and contains files..."
docker exec $container_id ls -la /home/sample-files
check_error "Failed to list contents of /home/sample-files in container."

# 2. Check if the /user/$username directory exists in HDFS and create it if necessary
echo "Checking if HDFS directory /user/$username exists..."
if ! docker exec $container_id hdfs dfs -test -e /user/$username; then
    echo "Creating HDFS directory /user/$username..."
    docker exec $container_id hdfs dfs -mkdir /user/$username
    check_error "Failed to create HDFS directory /user/$username."
else
    echo "HDFS directory /user/$username already exists. Skipping creation."
fi

# 3. Check if the user exists and skip creation if it does
echo "Checking if user $username exists..."
if docker exec $container_id id -u $username &>/dev/null; then
    echo "User $username already exists. Skipping user creation."
else
    echo "Creating user $username..."
    docker exec $container_id useradd -m $username
    check_error "Failed to create user $username."
fi

# Optional: Set password for the user (if needed)
# Uncomment the next line if you want to set a password.
# docker exec $container_id passwd $username
# check_error "Failed to set password for $username."

# 4. Change the ownership of the directory to user $username
echo "Changing ownership of /user/$username to $username..."
docker exec $container_id hdfs dfs -chown $username:$username /user/$username
check_error "Failed to change ownership of /user/$username."

# 5. Check if the /user/$username/sample-files directory exists in HDFS and create it if necessary
echo "Checking if /user/$username/sample-files exists in HDFS..."
if ! docker exec $container_id hdfs dfs -test -e /user/$username/sample-files; then
    echo "Creating the /user/$username/sample-files directory in HDFS..."
    docker exec $container_id hdfs dfs -mkdir /user/$username/sample-files
    check_error "Failed to create HDFS directory /user/$username/sample-files."
else
    echo "/user/$username/sample-files already exists. Skipping creation."
fi

# 6. Open an interactive shell inside the container to manually upload files to HDFS
echo "Opening interactive shell inside the container to manually upload files to HDFS..."
docker exec -it $container_id /bin/bash

# Inside the shell, the user should run the following command to upload selected file:
# hdfs dfs -put /home/sample-files/image_data.json /user/imager/sample-files/
# hdfs dfs -put /home/sample-files/image_data.csv /user/imager/sample-files/
# hdfs dfs -put /home/sample-files/image_data.yaml /user/imager/sample-files/
# hdfs dfs -put /home/sample-files/image_data.parquet /user/imager/sample-files/

# The user will need to manually run the above command to upload the files from the container to HDFS.

# 7. Confirm successful upload (this part is outside the interactive shell)
echo "Interactive shell opened. After running the upload command, the script will finish."

# When the user exits the interactive shell, the script ends.
