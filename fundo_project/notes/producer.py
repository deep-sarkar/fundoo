from kafka import KafkaProducer
import json
import os

client = os.environ['KAFKA_CLIENT']
producer = KafkaProducer(bootstrap_servers=client)

def add_reminders_to_queue(email,data):
    message = "reminder added"
    if len(email)!= 0:
        message ={
            "email":str(email),
            "title":data.get("title"),
            "reminder":data.get("reminder")
        }
        username = data.get('user_id')
        producer.send("reminders",json.dumps(message).encode('utf-8'))