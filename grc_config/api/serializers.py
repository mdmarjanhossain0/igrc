from rest_framework import serializers
from grc_config.models import (
    StatusDB,
    RiskSource,
    ReviewStatus,
    LikelyHood,
    Impact,
    PlanningStrategy,
    MitigationEffort,
    RiskStatus,
    NextStep,
    DataClassifiation
)

class StatusDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusDB
        fields = '__all__'

class RiskSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskSource
        fields = '__all__'

class ReviewStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewStatus
        fields = '__all__'

class LikelyHoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikelyHood
        fields = '__all__'

class ImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impact
        fields = '__all__'

class PlanningStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningStrategy
        fields = '__all__'

class MitigationEffortSerializer(serializers.ModelSerializer):
    class Meta:
        model = MitigationEffort
        fields = '__all__'

class RiskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskStatus
        fields = '__all__'

class NextStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextStep
        fields = '__all__'

class DataClassifiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataClassifiation
        fields = '__all__'
