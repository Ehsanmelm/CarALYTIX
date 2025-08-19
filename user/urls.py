from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *
app_name = 'user'
urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='register'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/logout/', LogoutView.as_view(), name='logout'),
    path('train-model/', TrainModelView.as_view(), name='train_model'),
    path('user/predict-price/', CarPricePredictView.as_view(), name='predict-price'),
    path('user/suggest-car/', SuggestCarsByPriceView.as_view(),
         name='suggest_car_by_price'),
]
