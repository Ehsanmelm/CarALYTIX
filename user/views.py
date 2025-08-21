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
    serializer_class = UserRegisterSerializer

    def post(self, request):
        # request.data["role"] = Role.objects.get(name="admin").id
        role = Role.objects.get(name="admin")
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['role'] = role
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
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        pass


class TrainModelView(APIView):
    def post(self, request):
        cars = Car.objects.filter(
        )

        serializer = CarTrainSerializer(cars, many=True)
        data = serializer.data
        df = pd.DataFrame(data)
        X = df[['name', 'model', 'gearbox', 'year',
                'mile', 'body_health', 'engine_status']]
        y = df['price']

        X_encoded = pd.get_dummies(X)

        model = LinearRegression()
        model.fit(X_encoded, y)

        joblib.dump(model, 'car_price_model.pkl')
        joblib.dump(X_encoded.columns, 'model_columns.pkl')

        return Response({"message": "model trained successfully"}, status=status.HTTP_200_OK)


class CarPricePredictView(APIView):
    serializer_class = CartPricePredicateSerializer

    def post(self, request):
        try:
            serializers = CartPricePredicateSerializer(data=request.data)
            serializers.is_valid(raise_exception=True)

            # data = request.data
            input_data = {
                'name': serializers.validated_data.get("name", None),
                'model': serializers.validated_data.get('model', None),
                'gearbox': serializers.validated_data.get('gearbox', None),
                'year': serializers.validated_data.get('year', None),
                'mile': float(serializers.validated_data.get('mile', None)),
                'body_health': serializers.validated_data.get('body_health', None),
                'engine_status':serializers.validated_data.get('engine_status', None),
            }

            model = joblib.load('car_price_model.pkl')
            model_columns = joblib.load('model_columns.pkl')

            input_df = pd.DataFrame([input_data])

            input_encoded = pd.get_dummies(input_df)
            input_encoded = input_encoded.reindex(
                columns=model_columns, fill_value=0)

            predicted_price = model.predict(input_encoded)[0]

            return Response({'predicted_price': round(predicted_price, 2)})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SuggestCarsByPriceView(APIView):
    serializer_class = SuggestCarSerialzier

    def post(self, request):
        try:
            serializer = SuggestCarSerialzier(data=request.data)
            serializer.is_valid(raise_exception=True)

            target_price = float(serializer.validated_data.get('price', 0))
            tolerance = 0.1

            if target_price <= 0:
                return Response({"error": "Price must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

            model = joblib.load('car_price_model.pkl')
            model_columns = joblib.load('model_columns.pkl')

            cars = Car.objects.all()
            serializer = CartPricePredicateSerializer(cars, many=True)
            df = pd.DataFrame(serializer.data)

            if df.empty:
                return Response({"message": "No cars found in database."}, status=status.HTTP_404_NOT_FOUND)

            X = df[['name', 'model', 'gearbox', 'year',
                    'mile', 'body_health', 'engine_status']]
            X_encoded = pd.get_dummies(X)
            X_encoded = X_encoded.reindex(columns=model_columns, fill_value=0)

            df['predicted_price'] = model.predict(X_encoded)

            lower_bound = target_price * (1 - tolerance)
            upper_bound = target_price * (1 + tolerance)
            suggested_cars = df[(df['predicted_price'] >= lower_bound) & (
                df['predicted_price'] <= upper_bound)]

            result = suggested_cars.to_dict(orient='records')

            return Response({"suggested_cars": result})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UniqueCarNamesAPIView(APIView):
    def get(self, request):
        unique_names = Car.objects.values_list('name', flat=True).distinct()
        data = [{'name': name} for name in unique_names if name]
        return Response(data, status=status.HTTP_200_OK)

class CarModelsByNameAPIView(APIView):
    def get(self, request):
        car_name = request.query_params.get('name')
        if not car_name:
            return Response({'error': 'name query param is required'}, status=status.HTTP_400_BAD_REQUEST)

        unique_models = Car.objects.filter(name=car_name).values_list('model', flat=True).distinct()
        data = [{'model': model} for model in unique_models if model]
        return Response(data, status=status.HTTP_200_OK)