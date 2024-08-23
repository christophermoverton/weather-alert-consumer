# Weather Alert Consumer

This project sets up a Kafka consumer that listens to a Kafka topic for weather alerts, stores them in MongoDB, and deletes expired alerts automatically. This project is designed to work seamlessly with the Kafka weather alert producer available at [docker_kafka_weatheralert](https://github.com/christophermoverton/docker_kafka_weatheralert).

## Prerequisites

- Docker
- Kafka and Zookeeper running on an external network.
- MongoDB for storing weather alerts.

## Setup

1. Clone this repository.
2. Ensure Kafka and Zookeeper are running on the external network.
3. Clone and set up the Kafka weather alert producer from the [docker_kafka_weatheralert](https://github.com/christophermoverton/docker_kafka_weatheralert) repository:
   ```bash
   git clone https://github.com/christophermoverton/docker_kafka_weatheralert.git
   cd docker_kafka_weatheralert
   docker-compose up -d
   ```
4. Create an external Docker network if one doesn't exist:
   ```bash
   docker network create kafka-network
   ```
5. Update `.env` with the correct Kafka broker address.
6. Build and run the Docker containers for the consumer and MongoDB:
   ```bash
   docker-compose up --build
   ```

## Services

- **MongoDB**: Stores the weather alerts.
- **Consumer**: Consumes weather alerts from Kafka and inserts them into MongoDB.

## MongoDB Storage Information

### MongoDB Data Directory

By default, MongoDB stores its data files in the `data/mongo/` directory. These files include collections, indexes, and metadata for the database. When MongoDB is running inside a Docker container, the `data/mongo/` directory is mounted as a volume to ensure that data persists even when the container is stopped or removed.

- **Location**: `data/mongo/`
- **Purpose**: This directory contains all the database files for MongoDB, including:
  - Collections (e.g., `collection-*.wt` files)
  - Indexes (e.g., `index-*.wt` files)
  - WiredTiger storage engine files (e.g., `WiredTiger*`)
  - Lock and state files (e.g., `mongod.lock`)
  - Metadata (e.g., `storage.bson`)

### Managing MongoDB Storage

If you need to reset the MongoDB data (e.g., for testing or debugging purposes), you can safely delete the contents of the `data/mongo/` directory, but only **after stopping the MongoDB container**.

1. **Stop the MongoDB Container**:
   Before attempting to remove the data, ensure the MongoDB container is stopped:
   ```bash
   docker-compose stop mongo
   ```

2. **Remove the Data**:
   You can then remove the contents of the `data/mongo/` directory:
   ```bash
   rm -rf data/mongo/*
   ```

3. **Restart the Containers**:
   After clearing the data, restart the containers:
   ```bash
   docker-compose up --build
   ```

   MongoDB will recreate the necessary files when it starts.

### Important Notes

- **Persistence**: The `data/mongo/` directory is mounted as a volume to ensure that MongoDB data persists across container restarts. If you remove the contents of this directory, all stored alerts will be lost.
- **Permissions**: The files in the `data/mongo/` directory are created and managed by the MongoDB process, which may result in permission issues when attempting to remove or modify the files. If you encounter permission errors, you may need to change the ownership of the directory or use `sudo` to manage the files.

## Integration with [docker_kafka_weatheralert](https://github.com/christophermoverton/docker_kafka_weatheralert)

This project is intended to work alongside the [docker_kafka_weatheralert](https://github.com/christophermoverton/docker_kafka_weatheralert) repository, which produces weather alerts and sends them to a Kafka topic. The consumer in this project listens to that Kafka topic and processes the alerts by storing them in MongoDB.

### Steps to Integrate:

1. **Run the Kafka Weather Alert Producer**:
   Follow the instructions in the [docker_kafka_weatheralert](https://github.com/christophermoverton/docker_kafka_weatheralert) repository to start the Kafka weather alert producer. This will start sending weather alerts to a Kafka topic.

2. **Configure the Consumer**:
   Ensure that the `KAFKA_BOOTSTRAP_SERVERS` environment variable in the `.env` file of this repository is set to the correct Kafka broker address used by the Kafka weather alert producer.

3. **Start the Consumer**:
   Run this project's Docker containers. The consumer will automatically start listening to the Kafka topic for new weather alerts and store them in MongoDB.

### Testing the Integration:

- **Verify Alerts in MongoDB**:
  After running both the producer and the consumer, you can connect to MongoDB and verify that weather alerts are being stored correctly.

- **Check MongoDB Collections**:
  You can inspect the MongoDB collections to ensure that the data is being stored as expected and that expired alerts are being removed as designed.

## Clean-up

Expired alerts are deleted every minute by the consumer service based on the `expires` field in the MongoDB documents.

To manually remove expired data, you can use the MongoDB shell to query and delete records.

```bash
docker exec -it mongo mongo --eval 'db.alerts.remove({"expires": {"$lt": new Date()}})'
```

## Troubleshooting MongoDB Storage Issues

If you encounter issues with MongoDB storage (e.g., unable to delete files due to permissions), here are a few tips:

- **File Permissions**: You can change the ownership of the `data/mongo/` directory to your user by running:
  ```bash
  sudo chown -R $USER:$USER data/mongo/
  ```
- **Locked Files**: Ensure that the MongoDB container is stopped before attempting to remove or modify files in the `data/mongo/` directory.

## Conclusion

This project demonstrates the use of Docker to run a Kafka consumer that processes weather alerts and stores them in MongoDB. By using Docker volumes, MongoDB data can persist across container restarts, and the system can be scaled and managed with ease. It is designed to integrate with the Kafka weather alert producer found in the [docker_kafka_weatheralert](https://github.com/christophermoverton/docker_kafka_weatheralert) repository.

