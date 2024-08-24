#!/bin/bash

# Get the MongoDB container ID (replace <mongo-container-name> with your MongoDB container name)
MONGO_CONTAINER=$(docker ps -qf "name=weather-alert-consumer-mongo-1")
# Check if the MongoDB container is running
if [ -z "$MONGO_CONTAINER" ]; then
  echo "MongoDB container is not running. Please start the container."
  exit 1
fi

# Run the init-mongo.js script inside the MongoDB container
echo "Running init-mongo.js inside the MongoDB container..."
docker exec -it $MONGO_CONTAINER mongo admin --eval 'load("/docker-entrypoint-initdb.d/init-mongo.js")'

# Verify that the user was created successfully
echo "Verifying the created users..."
docker exec -it $MONGO_CONTAINER mongo admin --eval 'db.getUsers()'

echo "Initialization script executed successfully."
