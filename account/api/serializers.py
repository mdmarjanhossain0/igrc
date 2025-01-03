from rest_framework import serializers

from account.models import (
    Account
)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Account
        fields = [
            "email",
            "username",
            "profile_picture",
            "role",
            "password",
        ]

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        # fields = "__all__"
        exclude = ["groups", "user_permissions",'password','otp','otp_send_time','is_verified','verified_at','tenant_limit','is_active','is_staff','is_superuser','is_admin','last_login','date_joined',]
