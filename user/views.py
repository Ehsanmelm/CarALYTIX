from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from role.models import Role
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

