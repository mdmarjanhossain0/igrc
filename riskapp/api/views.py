from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from django.utils import timezone
import requests

from mysite.constants.status_constants import(
	SUCCSS,
	ERROR
)
from account.api.utils import (
	mobile_check,
	generate_otp
)
from account.models import (
	Account,
)

from account.api.serializers import (
	AccountSerializer,
	RegisterSerializer,
	LoginSerializer
)

from drf_yasg.utils import swagger_auto_schema
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
from riskapp.api.serializers import (
	RiskMappingSerializer,
    ThreatMappingSerializer,
    RiskCategorySerializer,
    RiskScoringMethodSerializer,
    ControlRegisterSerializer,
    TeamSerializer,
    RiskRegisterSerializer,
    MitigationControlSerializer,
    RiskMitigationSerializer,
    ReviewSerializer,
    PlanProjectSerializer,
    ReviewProjectSerializer,
    CommentSerializer
)

class ProjectRiskListApiView(ListAPIView):
	serializer_class = RiskRegisterSerializer
	permission_classes = [IsAuthenticated]
	def get_queryset(self):
		project_id = self.kwargs.get('project_id')
		return RiskRegister.objects.filter(control__project_id=project_id)
	