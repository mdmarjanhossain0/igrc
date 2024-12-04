from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RiskMappingModelViewSet,
    ThreatMappingModelViewSet,
    RiskCategoryModelViewSet,
    RiskScoringMethodModelViewSet,
    ControlRegisterModelViewSet,
    TeamModelViewSet,
    RiskRegisterModelViewSet,
    MitigationControlModelViewSet,
    RiskMitigationModelViewSet,
    ReviewModelViewSet,
    PlanProjectModelViewSet,
    ReviewProjectModelViewSet,
    CommentModelViewSet
)
app_name = 'riskapp_api'

router = DefaultRouter()
router.register(r'risk-mapping', RiskMappingModelViewSet)
router.register(r'threat-mapping', ThreatMappingModelViewSet)
router.register(r'risk-category', RiskCategoryModelViewSet)
router.register(r'risk-scoring-method', RiskScoringMethodModelViewSet)
router.register(r'control-register', ControlRegisterModelViewSet)
router.register(r'team', TeamModelViewSet)
router.register(r'risk-register', RiskRegisterModelViewSet)
router.register(r'mitigation-control', MitigationControlModelViewSet)
router.register(r'risk-mitigation', RiskMitigationModelViewSet)
router.register(r'review', ReviewModelViewSet)
router.register(r'plan-project', PlanProjectModelViewSet)
router.register(r'review-project', ReviewProjectModelViewSet)
router.register(r'comment', CommentModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
