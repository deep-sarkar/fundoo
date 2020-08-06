from kafka import KafkaConsumer
from json import loads
import json
import os
from datetime import datetime
from time import sleep
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler

clint = os.environ['KAFKA_CLINT']
scheduler = BackgroundScheduler()
scheduler.start()


def send_mail(data):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    subject = "You have remiinder at {}".format(data['reminder'])
    body    = data['title']
    message = 'Subject: {}\n\n{}'.format(subject, data['title'])
    server.sendmail(EMAIL_HOST_USER, data['email'], message)
    scheduler.remove_job(data['job_id'])
    print("success")
  


def kafka_consumer():
    consumer = KafkaConsumer('reminders', bootstrap_servers=clint)
    job_id = 0
    for task in consumer:
        new_task = task.value
        data = json.loads(new_task.decode('utf-8'))
        now = datetime.now()
        total_remaining_time = data['reminder'].split(':')
        job_id += 1
        data['job_id'] = str(job_id)
        hours   = total_remaining_time[0]
        minutes = total_remaining_time[1]
        scheduler.add_job(send_mail,'cron', kwargs={"data":data}, hour=hours, minute=minutes, id=data['job_id'])

kafka_consumer()