from rest_framework import viewsets
from app.models import Framework

import rest_framework.decorators
from .serializers import FrameWorkSerializer


class FrameWorkModelViewSet(viewsets.ModelView):
  queryset=Framework.objects.all()
  serializer_class=FrameWorkSerializer




