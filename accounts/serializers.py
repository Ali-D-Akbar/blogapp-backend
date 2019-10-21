from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                validated_data['username'], validated_data['email'],
                validated_data['password']
            )
            return user
        except KeyError:
            raise (serializers.ValidationError("one or more values missing"))


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        else:
            raise (serializers.ValidationError("Incorrect Credentials"))
