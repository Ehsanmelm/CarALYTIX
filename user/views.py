from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from role.models import Role
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from django.db.models import Q
from scrap.models import Car

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        request.data["role"]=Role.objects.get(name="admin").id
        serializer = UserRegisterSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if serializer.validated_data['password']:
            user.set_password(serializer.validated_data['password'])
            user.save()
        refresh = RefreshToken.for_user(user)
        context = {
            'full_name': user.first_name + ' ' + user.last_name,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(context, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self,request):
        pass


class TrainModelView(APIView):

    def post(self,request):
        cars = Car.objects.filter(
        )

        serializer = CarTrainSerializer(cars, many=True)
        data = serializer.data
        df = pd.DataFrame(data)
        X = df[['name','model', 'gearbox', 'year', 'mile', 'body_health']]
        y = df['price']

        X_encoded = pd.get_dummies(X)

        model = LinearRegression()
        model.fit(X_encoded, y)

        joblib.dump(model, 'car_price_model.pkl')
        joblib.dump(X_encoded.columns, 'model_columns.pkl')

        return Response({"message":"model trained successfully"},status=status.HTTP_200_OK)

    

class CarPricePredictView(APIView):
    def post(self, request):
        try:
            data = request.data
            input_data = {
                'name':data.get("name"),
                'model': data.get('model'),
                'gearbox': data.get('gearbox'),
                'year': data.get('year'),
                'mile': float(data.get('mile')),
                'body_health': data.get('body_health'),
            }

            model = joblib.load('car_price_model.pkl')
            model_columns = joblib.load('model_columns.pkl')

            input_df = pd.DataFrame([input_data])

            input_encoded = pd.get_dummies(input_df)
            input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

            predicted_price = model.predict(input_encoded)[0]

            return Response({'predicted_price': round(predicted_price, 2)})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


