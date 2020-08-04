from kafka import KafkaConsumer
from json import loads
import json
import os
from datetime import datetime
from time import sleep
import smtplib

clint = os.environ['KAFKA_CLINT']

def send_mail(data):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    subject = "You have remiinder at {}".format(data['reminder'])
    body    = data['title']
    message = 'Subject: {}\n\n{}'.format(subject, data['title'])
    server.sendmail(EMAIL_HOST_USER, data['email'], message)
    


def kafka_consumer():
    consumer = KafkaConsumer('reminders', bootstrap_servers=clint)
    for task in consumer:
        new_task = task.value
        new_task_dict = json.loads(new_task.decode('utf-8'))
        now = datetime.now()
        current_time = datetime.strptime(now.strftime("%H:%M"),"%H:%M")
        reminder_time = datetime.strptime(new_task_dict['reminder'],"%H:%M")
        remaining_time = reminder_time - current_time
        seconds = remaining_time.total_seconds()
        sleep(seconds)
        send_mail(new_task_dict)
    

kafka_consumer()