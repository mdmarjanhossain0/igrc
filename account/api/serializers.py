from rest_framework import serializers

from account.models import (
    Account,
    Organization
)


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            "mobile",
            "username",
            "profile_picture",
            "role",
            "region",
            "district",
            "institution",
            "occupation"
        ]

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        # fields = "__all__"
        exclude = ["groups", "user_permissions"]

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"
