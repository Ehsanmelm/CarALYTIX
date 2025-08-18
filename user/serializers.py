from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken    

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['password','email','first_name','last_name','role']
        extra_kwargs = {'password' : {'write_only' : True}}

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,required=True)
    password = serializers.CharField(write_only=True, required=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    user = None

    def validate(self, attrs):
        email = attrs["email"]
        self.password = attrs["password"]
        self.user = CustomUser.objects.filter(email=email).last()

        if self.user is None or  not self.user.check_password(attrs["password"]):
            raise serializers.ValidationError("username or Password is wrong")

        return {}

    def create(self, validated_data):
        refresh = RefreshToken.for_user(self.user)
        validated_data["refresh"] = str(refresh)
        validated_data["access"] = str(refresh.access_token)
        return validated_data