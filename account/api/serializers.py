from rest_framework import serializers

from account.models import (
    Account
)


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            "email",
            "username",
            "profile_picture",
            "role",
        ]

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        # fields = "__all__"
        exclude = ["groups", "user_permissions"]
