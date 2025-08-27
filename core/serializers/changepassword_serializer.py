from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password']
        extra_kwargs = {'password': {'write_only': True}}
