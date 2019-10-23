from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response

from accounts.serializers import LoginSerializer, RegisterSerializer, UserSerializer


# Register API
class RegisterAPI(generics.GenericAPIView):
    """
    This view provides a post request to register a user.
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Post request method to register a user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(
                user, context=self.get_serializer_context()
            ).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    """
    This view provides a post request to Login a user.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Post request method to login a user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(
                user, context=self.get_serializer_context()
            ).data,
            "token": AuthToken.objects.create(user)[1]
        })


# User API
class UserAPI(generics.RetrieveAPIView):
    """
    This view provides `list` and `detail` read-only actions.
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        """
        Gets the currently logged in user.
        """
        return self.request.user
