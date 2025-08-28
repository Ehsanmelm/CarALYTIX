# scrap/tasks.py
from celery import shared_task
from .models import Client


@shared_task
def run_all_scrapers():
    for client in Client.objects.all():
        client.run_script()
