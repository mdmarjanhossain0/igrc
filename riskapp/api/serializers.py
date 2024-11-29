from rest_framework import serializers

from account.models import (
    Account
)

from riskapp.models import (
    RiskMapping,
    ThreatMapping,
    RiskCategory,
    RiskScroingMethod,
    ControlRegister,
    Team,

    RiskRegister,
    MitigationControl,
    RiskMitigation,
    Review,
    PlanProject,
    ReviewProject,
    Comment
)

class RiskMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskMapping
        fields = "__all__"

class ThreatMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThreatMapping
        fields = "__all__"

class RiskCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskCategory
        fields = "__all__"

class RiskScoringMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskScroingMethod
        fields = "__all__"


class ControlRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ControlRegister
        fields = "__all__"
class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = "__all__"
class RiskRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskRegister
        fields = "__all__"
class MitigationControlSerializer(serializers.ModelSerializer):

    class Meta:
        model = MitigationControl
        fields = "__all__"

class RiskMitigationSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskMitigation
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"

class PlanProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanProject
        fields = "__all__"

class ReviewProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewProject
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"