from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StatusDBModelViewSet,
    RiskSourceModelViewSet,
    ReviewStatusModelViewSet,
    LikelyHoodModelViewSet,
    ImpactModelViewSet,
    PlanningStrategyModelViewSet,
    MitigationEffortModelViewSet,
    RiskStatusModelViewSet,
    NextStepModelViewSet,
    DataClassifiationModelViewSet
)
app_name = 'grc_config_app_api'

router = DefaultRouter()
router.register(r'statusdb', StatusDBModelViewSet)
router.register(r'risksource', RiskSourceModelViewSet)
router.register(r'reviewstatus', ReviewStatusModelViewSet)
router.register(r'likelyhood', LikelyHoodModelViewSet)
router.register(r'impact', ImpactModelViewSet)
router.register(r'planningstrategy', PlanningStrategyModelViewSet)
router.register(r'mitigationeffort', MitigationEffortModelViewSet)
router.register(r'riskstatus', RiskStatusModelViewSet)
router.register(r'nextstep', NextStepModelViewSet)
router.register(r'dataclassifiation', DataClassifiationModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
