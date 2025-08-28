# tasks.py
from celery import shared_task


@shared_task
def train_car_price_model():
    from user.views import TrainModelView
    from rest_framework.test import APIRequestFactory

    factory = APIRequestFactory()
    request = factory.post("/train-model/")
    view = TrainModelView.as_view()
    response = view(request)
    return response.data
