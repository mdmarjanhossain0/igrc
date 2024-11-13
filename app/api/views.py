from rest_framework import viewsets
from app.models import (Clause, Control, Framework, Policy, Project, ProjectClause, ProjectControl,
    ProjectMember, ProjectTask, SubControl, Task, TenantPolicy)
from .serializers import (
  FrameworkSerializer,
  TaskSerializer,
  ClauseSerializer,
  PolicySerializer,
  ControlSerializer,
  SubControlSerializer,
  ProjectSerializer,
  ProjectMemberSerializer,
  ProjectTaskSerializer,
  ProjectClauseSerializer,
  TenantPolicySerializer,
  ProjectControlSerializer
)

class FrameworkModelViewSet(viewsets.ModelViewSet):
    queryset = Framework.objects.all()
    serializer_class = FrameworkSerializer

class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class ClauseModelViewSet(viewsets.ModelViewSet):
    queryset = Clause.objects.all()
    serializer_class = ClauseSerializer

class PolicyModelViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

class ControlModelViewSet(viewsets.ModelViewSet):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer

class SubControlViewSet(viewsets.ModelViewSet):
    queryset = SubControl.objects.all()
    serializer_class = SubControlSerializer


class ProjectModelViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectMemberModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer

class ProjectTaskModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer

class ProjectClauseModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectClause.objects.all()
    serializer_class = ProjectClauseSerializer

class TenantPolicyModelViewSet(viewsets.ModelViewSet):
    queryset = TenantPolicy.objects.all()
    serializer_class = TenantPolicySerializer

class ProjectControlModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectControl.objects.all()
    serializer_class = ProjectControlSerializer
