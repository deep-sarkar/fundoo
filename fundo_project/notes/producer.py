from kafka import KafkaProducer
import json
import os

clint = os.environ['KAFKA_CLINT']

def add_reminders_to_queue(email,data):
    producer = KafkaProducer(bootstrap_servers=clint)
    message = "reminder added"
    if len(email)!= 0:
        message ={
            "email":str(email),
            "Title":data.get("title"),
            "Reminder":data.get("reminder")
        }
        username = data.get('user_id')
        producer.send("notes",json.dumps(message).encode('utf-8'))