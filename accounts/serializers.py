from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the data of a user.
    """

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializes the data to register a user using POST request.
    """

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Handles the validated data to create a user.
        """
        try:
            user = User.objects.create_user(
                validated_data['username'], validated_data['email'], validated_data['password']
            )
            return user
        except KeyError:
            raise (serializers.ValidationError("one or more values missing"))


# Login Serializer
class LoginSerializer(serializers.Serializer):
    """
    Serializes the data to login a user using POST request.
    """

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validates the data based on username and password.
        """
        user = authenticate(**data)
        if user and user.is_active:
            return user
        else:
            raise (serializers.ValidationError("Incorrect Credentials"))
