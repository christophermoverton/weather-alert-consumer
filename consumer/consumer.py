from confluent_kafka import Consumer, KafkaException, KafkaError
from pymongo import MongoClient
from datetime import datetime
import time
import json

# Retry logic for Kafka connection
def connect_to_kafka(conf):
    while True:
        try:
            consumer = Consumer(conf)
            consumer.subscribe(['weather-alerts'])
            return consumer
        except Exception as e:
            print(f"Error connecting to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'weather-alert-consumers',
    'auto.offset.reset': 'earliest'
}

# MongoDB connection
mongo_client = MongoClient("mongodb://mongo:27017/")
db = mongo_client.weather_alerts_db
alerts_collection = db.alerts

consumer = connect_to_kafka(kafka_conf)

# Consume messages and store in MongoDB
def consume_and_store_alerts():
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        
        # Parse the message (Assuming JSON format)
        alert = msg.value().decode('utf-8')
        alert_data = json.loads(alert)
        
        # Insert the alert into MongoDB
        alerts_collection.insert_one(alert_data)
        print(f"Inserted alert: {alert_data}")

# Function to clean up expired alerts
def delete_expired_alerts():
    while True:
        now = datetime.utcnow()  # Get the current UTC time
        result = alerts_collection.delete_many({"expires": {"$lt": now}})
        if result.deleted_count > 0:
            print(f"Deleted {result.deleted_count} expired alerts")
        time.sleep(60)  # Check every minute for expired alerts

if __name__ == "__main__":
    try:
        # Run the consumer in the background
        consume_and_store_alerts()

        # Run the expired alert deletion as well
        delete_expired_alerts()

    except KeyboardInterrupt:
        pass
    finally:
        # Clean up the consumer before exiting
        consumer.close()
