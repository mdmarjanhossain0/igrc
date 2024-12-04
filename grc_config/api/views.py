from rest_framework import viewsets
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
from .serializers import (
    StatusDBSerializer,
    RiskSourceSerializer,
    ReviewStatusSerializer,
    LikelyHoodSerializer,
    ImpactSerializer,
    PlanningStrategySerializer,
    MitigationEffortSerializer,
    RiskStatusSerializer,
    NextStepSerializer,
    DataClassifiationSerializer
)


class StatusDBModelViewSet(viewsets.ModelViewSet):
    queryset = StatusDB.objects.all()
    serializer_class = StatusDBSerializer

class RiskSourceModelViewSet(viewsets.ModelViewSet):
    queryset = RiskSource.objects.all()
    serializer_class = RiskSourceSerializer

class ReviewStatusModelViewSet(viewsets.ModelViewSet):
    queryset = ReviewStatus.objects.all()
    serializer_class = ReviewStatusSerializer

class LikelyHoodModelViewSet(viewsets.ModelViewSet):
    queryset = LikelyHood.objects.all()
    serializer_class = LikelyHoodSerializer

class ImpactModelViewSet(viewsets.ModelViewSet):
    queryset = Impact.objects.all()
    serializer_class = ImpactSerializer

class PlanningStrategyModelViewSet(viewsets.ModelViewSet):
    queryset = PlanningStrategy.objects.all()
    serializer_class = PlanningStrategySerializer

class MitigationEffortModelViewSet(viewsets.ModelViewSet):
    queryset = MitigationEffort.objects.all()
    serializer_class = MitigationEffortSerializer

class RiskStatusModelViewSet(viewsets.ModelViewSet):
    queryset = RiskStatus.objects.all()
    serializer_class = RiskStatusSerializer

class NextStepModelViewSet(viewsets.ModelViewSet):
    queryset = NextStep.objects.all()
    serializer_class = NextStepSerializer

class DataClassifiationModelViewSet(viewsets.ModelViewSet):
    queryset = DataClassifiation.objects.all()
    serializer_class = DataClassifiationSerializer
