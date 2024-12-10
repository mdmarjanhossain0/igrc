import django.contrib.auth
from rest_framework import viewsets, status
from app.models import (Clause, Control, Evidence, EvidenceFile, Framework, Policy, Project,
    ProjectClause, ProjectControl, ProjectMember, ProjectSubControl, ProjectTask, SubControl, Task,
    Tenant, TenantPolicy)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.api.permissions import IsGrcAdmin, IsProjectAdmin, IsProjectManager, Or
from .serializers import (ClauseSerializer, ControlSerializer, ControlWithSubControlSerializer,
    EvidenceSerializer, FrameworkSerializer, PolicySerializer, ProjectClauseSerializer,
    ProjectControlSerializer, ProjectMemberSerializer, ProjectSerializer,
    ProjectSubControlSerializer, ProjectTaskSerializer, SubControlSerializer, TaskSerializer,
    TenantPolicySerializer, TenantSerializer, ProjectControlWithSubControlSerializer)

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes=[IsGrcAdmin]
        return super(TenantModelViewSet, self).get_permissions()






class ProjectModelViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes=[IsGrcAdmin]
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsProjectAdmin]
        
        return super(ProjectModelViewSet, self).get_permissions()


class ProjectMemberModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes=[(IsGrcAdmin)]
        return super(ProjectMemberModelViewSet, self).get_permissions()


    

class ProjectTaskModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer

class ProjectClauseModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectClause.objects.all()
    serializer_class = ProjectClauseSerializer

class TenantPolicyModelViewSet(viewsets.ModelViewSet):
    queryset = TenantPolicy.objects.all()
    serializer_class = TenantPolicySerializer

class ProjectPoicyModelViewSet(viewsets.ModelViewSet):
    queryset = TenantPolicy.objects.all()
    serializer_class = TenantPolicySerializer
    def get_queryset(self):
        return TenantPolicy.objects.filter(project__in=[self.kwargs.get('project_id')])

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

class EvidenceByProjectView(viewsets.ModelViewSet):
    serializer_class = EvidenceSerializer
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Evidence.objects.filter(project_id=project_id)
    


class ClausesByProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectClauseSerializer
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return ProjectClause.objects.filter(project_id=project_id)

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        return [Or(IsGrcAdmin,IsProjectAdmin,IsProjectManager)]

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id) 
        serializer.save(project=project)

    def perform_update(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)

    def perform_destroy(self, instance):
        instance.delete()
    

class ControlsByProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectControlSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [IsAuthenticated()]
        return [Or(IsGrcAdmin,IsProjectAdmin,IsProjectManager)]
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return ProjectControl.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)
    
    def perform_update(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)
    
    def perform_destroy(self, instance):
        instance.delete()
    

class SubControlsByProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSubControlSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [IsAuthenticated()]
        return [Or(IsGrcAdmin,IsProjectAdmin,IsProjectManager)]
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        control_id = self.kwargs.get('control_id')
        return ProjectSubControl.objects.filter(
            project_id=project_id, 
            project_control_id=control_id
        )
    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        control_id = self.kwargs.get('control_id')
        project = Project.objects.get(id=project_id)
        control = ProjectControl.objects.get(id=control_id)
        serializer.save(project=project, project_control=control)

    def perform_update(self, serializer):
        project_id = self.kwargs.get('project_id')
        control_id = self.kwargs.get('control_id')
        project = Project.objects.get(id=project_id)
        control = Control.objects.get(id=control_id)
        serializer.save(project=project, control=control)

    def perform_destroy(self, instance):
        instance.delete()
    



class ControlWithSubControlsByProjectView(viewsets.ModelViewSet):
    # def get(self, request, project_id):
    #     controls=ProjectControl.objects.filter(project_id=project_id)
    #     serializer=ProjectControlWithSubControlSerializer(controls, many=True,)
    #     return Response(serializer.data)
    serializer_class = ProjectControlWithSubControlSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), Or(IsGrcAdmin, IsProjectAdmin, IsProjectManager)]
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return ProjectControl.objects.filter(project_id=project_id)


    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)

    def perform_update(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)

    def perform_destroy(self, instance):
        instance.delete()



class TasksByProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectTaskSerializer

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [IsAuthenticated()]
        return [Or(IsGrcAdmin,IsProjectAdmin,IsProjectManager)]
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return ProjectTask.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)

    def perform_update(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)

    def perform_destroy(self, instance):
        instance.delete()
    

class ProjectMembersByProject(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return  [IsAuthenticated()]
        return [Or(IsGrcAdmin,IsProjectAdmin,IsProjectManager)]

    
    def get(self, request, project_id):
        project_members=ProjectMember.objects.filter(project_id=project_id)
        serializer=ProjectMemberSerializer(project_members, many=True,)
        print(str(IsProjectAdmin()))
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Add a new member to a project",
        request_body=ProjectMemberSerializer,
        responses={
            201: ProjectMemberSerializer,
            400: openapi.Response(description="Bad Request", examples={
                'application/json': {'detail': 'Invalid data'}
            })
        },
        tags=["Project Members"],
        operation_summary="Add Project Member"
    )
    def post(self, request, project_id):
        data = request.data.copy()
        data['project'] = project_id
        serializer = ProjectMemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ProjectMemberByProject(APIView):

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [Or(IsGrcAdmin,IsProjectAdmin,IsProjectManager)]
        else:
            return [IsAuthenticated()]


    def get(self, request, project_id, member_id):
        project_member=ProjectMember.objects.get(project_id=project_id, id=member_id)
        serializer=ProjectMemberSerializer(project_member)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=ProjectMemberSerializer,
        responses={
            201: ProjectMemberSerializer,
            400: openapi.Response(description="Bad Request", examples={
                'application/json': {'detail': 'Invalid data'}
            })
        },
        operation_summary="Add Project Member"
    )
    def put(self, request, project_id, member_id):
        try:
            project_member = ProjectMember.objects.get(project_id=project_id, id=member_id)
        except ProjectMember.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectMemberSerializer(project_member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, member_id):
        try:
            project_member = ProjectMember.objects.get(project_id=project_id, id=member_id)
        except ProjectMember.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        project_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



