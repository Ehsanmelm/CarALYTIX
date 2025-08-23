from django.urls import path, include, re_path

from .views import *
app_name = 'user'
urlpatterns = [
    path('khodro45/', Khodro45View.as_view(), name='khodro45'),
    path('hamrah-mechanic/', HamrahMechanicView.as_view(), name='hamrah_mechanic'),
    path('karnameh/', karnamehView.as_view(), name='karnameh'),

]