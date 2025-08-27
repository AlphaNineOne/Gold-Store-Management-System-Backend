from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
# from rest_framework import permissions
from rest_framework import status
from core.threads import send_mail
from django.conf import settings
User = get_user_model()


class ForgetPasswordView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email', '')
        if email == '':
            message = {'detail': 'Email is required to reset password'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            message = {'detail': 'User with this email does not exist'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        # send email
        subject = 'Password Reset Request'
        message = 'Hi {user.username}, Please use this link to reset your password http://'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail()
        return Response({'detail': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
