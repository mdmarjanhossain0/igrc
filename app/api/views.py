from rest_framework import viewsets
from app.models import (Clause, Control, Evidence, EvidenceFile, Framework, Policy, Project,
    ProjectClause, ProjectControl, ProjectMember, ProjectSubControl, ProjectTask, SubControl, Task,
    Tenant, TenantPolicy)
from .serializers import (ClauseSerializer, ControlSerializer, ControlWithSubControlSerializer,
    EvidenceSerializer, FrameworkSerializer, PolicySerializer, ProjectClauseSerializer,
    ProjectControlSerializer, ProjectMemberSerializer, ProjectSerializer,
    ProjectSubControlSerializer, ProjectTaskSerializer, SubControlSerializer, TaskSerializer,
    TenantPolicySerializer, TenantSerializer)

from rest_framework.views import APIView
from rest_framework.response import Response

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

class SubControlModelViewSet(viewsets.ModelViewSet):
    queryset = SubControl.objects.all()
    serializer_class = SubControlSerializer

class TenantModelViewSet(viewsets.ModelViewSet):
    queryset=Tenant.objects.all()
    serializer_class = TenantSerializer


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

class ProjectSubControlModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectSubControl.objects.all()
    serializer_class = ProjectSubControlSerializer


class EvidenceModelViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer

    def perform_create(self, serializer):
        evidence = serializer.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            evidence_file = EvidenceFile.objects.create(file=file)
            evidence.files.add(evidence_file)

class ClausesByProjectView(APIView):
    def get(self, request, project_id):
        clauses=Clause.objects.filter(projectclause__project_id=project_id)
        serializer=ClauseSerializer(clauses, many=True,)
        return Response(serializer.data)

class ControlsByProjectView(APIView):
    def get(self, request, project_id):
        controls=Control.objects.filter(projectcontrol__project_id=project_id)
        serializer=ControlSerializer(controls, many=True,)
        return Response(serializer.data)

class ControlWithSubControlsByProjectView(APIView):
    def get(self, request, project_id):
        controls=Control.objects.filter(projectcontrol__project_id=project_id)
        serializer=ControlWithSubControlSerializer(controls, many=True,)
        return Response(serializer.data)
    
class TasksByProjectView(APIView):
    def get(self, request, project_id):
        tasks=Task.objects.filter(projecttask__project_id=project_id)
        serializer=TaskSerializer(tasks, many=True,)
        return Response(serializer.data)
