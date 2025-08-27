from core.serializers import CreateUserSerializer
from rest_framework.generics import CreateAPIView
from django.http import Http404
from django.contrib.auth import authenticate

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from core.utils import get_tokens_for_user
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
User = get_user_model()
email = settings.EMAIL_HOST_USER


class RegistrationView(APIView):
    """REgister and login api instant """

    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        print(email)
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)

        return Response({
            "user": CreateUserSerializer(user).data,
            "Token": token

        })
