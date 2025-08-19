from django.urls import path, include, re_path

from .views import *
app_name = 'user'
urlpatterns = [
    path('khodro45/', Khodro45View.as_view(), name='khodro45'),

]