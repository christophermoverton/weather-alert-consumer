# Weather Alert Consumer

This project sets up a Kafka consumer that listens to a Kafka topic for weather alerts, stores them in MongoDB, and deletes expired alerts automatically.

## Prerequisites

- Docker
- Kafka and Zookeeper running on an external network.

## Setup

1. Clone this repository.
2. Ensure Kafka and Zookeeper are running on the external network.
3. Create an external Docker network if one doesn't exist:
   ```bash
   docker network create kafka-network
Update .env with the correct Kafka broker address.
Build and run the Docker containers:
bash
Copy code
docker-compose up --build
Services
MongoDB: Stores the weather alerts.
Consumer: Consumes weather alerts from Kafka and inserts them into MongoDB.
Clean-up
Expired alerts are deleted every minute by the consumer service.

yaml
Copy code

### 7. **Additional Notes on Volumes**

If you want MongoDB data to persist across container restarts, you can mount a volume for MongoDB data:

```yaml
mongo:
  image: mongo:4.4
  ports:
    - "27017:27017"
  networks:
    - kafka-network
  volumes:
    - ./data/mongo:/data/db
This will store MongoDB data in the local ./data/mongo directory on your host machine.

Summary of Setup
docker-compose.yml: Manages MongoDB and consumer services.
consumer.py: Kafka consumer logic, which processes weather alerts and manages expired alert deletion.
Dockerfile: Builds the Docker image for the consumer service.
requirements.txt: Lists the necessary Python packages.
.env: Holds environment variables (Kafka broker, MongoDB URI, etc.).
README.md: Documentation on how to set up and run the project.