from celery import shared_task
import time

@shared_task
def hello():
    time.sleep(20)
    print("Hello, world!")