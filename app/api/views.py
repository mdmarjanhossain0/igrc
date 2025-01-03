from django.db import models
import os
import django.contrib.auth
from rest_framework import viewsets, status

from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import (
	api_view,
	authentication_classes,
	permission_classes,
)

from app.models import (Clause, Comment, Control, Evidence, EvidenceFile, Framework, Policy,
	Project, ProjectClause, ProjectControl, ProjectMember, ProjectScratchpad, ProjectSubControl,
	ProjectTask, SubControl, Task, Tenant, TenantPolicy, Note, AuditorFeedback, Comment,  ContextFile)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.api.permissions import IsGrcAdmin, IsProjectAdmin, IsProjectManager, IsTenantOwner, Or
from .serializers import (AuditorFeedbackSerializer, AuditorSummarySerrializer, ClauseSerializer,
	CommentSerializer, ContextFileSerializer, ControlAddToProjectSerializer, ControlSerializer,
	EvidenceAddToProjectTaskSerializer, EvidenceSerializer, FrameworkSerializer,
	NormativeReferencesSerializer, NoteSerializer, PolicyAddToProjectSerializer, PolicySerializer,
	ProjectClauseSerializer, ProjectControlSerializer, ProjectControlWithSubControlSerializer,
	ProjectMemberSerializer, ProjectScratchpadSerializer, ProjectSerializer, ProjectStatusSerializer,
	ProjectSubControlSerializer, ProjectTaskSerializer, SubControlSerializer, TaskSerializer,
	TenantPolicySerializer, TenantSerializer)
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.api.utils import (
	EvidenceFilterSet
)
from drf_yasg.utils import swagger_auto_schema



from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

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
	pagination_class=None
	serializer_class = TenantSerializer

	def get_permissions(self):
		if self.action in ['create', 'update', 'partial_update', 'destroy']:
			self.permission_classes=[IsGrcAdmin]
		return super(TenantModelViewSet, self).get_permissions()
	
	def list(self, request, *args, **kwargs):
			queryset = self.get_queryset()
			serializer = self.get_serializer(queryset, many=True)
			response_data = {
					'results': serializer.data
			}
			return Response(response_data)



class NoteViewSet(viewsets.ModelViewSet):
	queryset = Note.objects.all()
	serializer_class = NoteSerializer


class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	
class AditorFeedBackViewSet(viewsets.ModelViewSet):
	queryset = AuditorFeedback.objects.all()
	serializer_class = AuditorFeedbackSerializer

class ProjectModelViewSet(viewsets.ModelViewSet):
	queryset = Project.objects.all().order_by("-pk")
	serializer_class = ProjectSerializer
	
	def get_permissions(self):

		if self.action in ['list','retrieve']:
			return [IsAuthenticated()]
		if self.action == 'create':
			return [Or(IsGrcAdmin,IsProjectAdmin,IsTenantOwner)]
		if self.action in ['update', 'partial_update', 'destroy']:
			return [IsGrcAdmin()]
		return [Or(IsGrcAdmin,IsProjectAdmin,IsProjectManager,IsTenantOwner)]
		


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
	pagination_class=None

	def get_queryset(self):
		tenant_id = self.kwargs.get('tenant_id', None)
		if tenant_id:
			return TenantPolicy.objects.filter(tenant_id=tenant_id).values('policy_id').distinct()
		# else:
		# 	return TenantPolicy.objects.all()
	
	def list(self, request, *args, **kwargs):
			queryset = self.get_queryset()
			serializer = self.get_serializer(queryset, many=True)
			response_data = {
					'results': serializer.data
			}
			return Response(response_data)


class ProjectPoicyModelViewSet(viewsets.ModelViewSet):
	queryset = TenantPolicy.objects.all()
	serializer_class = TenantPolicySerializer
	def get_queryset(self):
		# Check if the request method is PUT or PATCH
		if self.request.method in ['PUT', 'PATCH']:
			return TenantPolicy.objects.all()
		# Default behavior for other methods
		return TenantPolicy.objects.filter(project__in=[self.kwargs.get('project_id')])
	
	def partial_update(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectControlModelViewSet(viewsets.ModelViewSet):
	queryset = ProjectControl.objects.all()
	serializer_class = ProjectControlWithSubControlSerializer
	pagination_class = None
	def get_queryset(self):
		tenant_id = self.kwargs.get('tenant_id', None)
		# print(tenant_id)
		if tenant_id:
			return ProjectControl.objects.filter(project__tenant_id=tenant_id).distinct()
		else:
			return ProjectControl.objects.all()
	
	def list(self, request, *args, **kwargs):
			queryset = self.get_queryset()
			serializer = self.get_serializer(queryset, many=True)
			response_data = {
					'results': serializer.data
			}
			return Response(response_data)


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
		return Evidence.objects.filter(project__in=project_id)
	


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
	http_method_names = ['get', 'post', 'patch', 'put', 'delete'] 
	def get_permissions(self):
		if self.action in ['list','retrieve']:
			return [IsAuthenticated()]
		return [Or(IsGrcAdmin,IsProjectAdmin,IsProjectManager,IsAdminUser())]
	
	def get_queryset(self):
		project_id = self.kwargs.get('project_id')
		return ProjectControl.objects.filter(project__in=project_id)

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
		return ProjectControl.objects.filter(project__id=project_id)


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
	pagination_class = None
	def get_permissions(self):
		if self.action in ['list','retrieve', 'update','partial_update']:
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
		# serializer.save(project=project)
		user = self.request.user
		instance = serializer.instance

		if user.role == "Admin" or user == project.owner:
			serializer.save(project=project)
   
		elif instance.assignee == user:
			update_data = self.request.data
			if 'completion' in update_data:
				instance.completion = update_data.get('completion')
				return Response({"message":"Updated Successfully"}, status=status.HTTP_200_OK)
			if 'context' in update_data:
				instance.completion = update_data.get('context')
				return Response({"message":"Updated Successfully"}, status=status.HTTP_200_OK)

			raise PermissionDenied("You are only allowed to update the completion field.")
	
	def perform_destroy(self, instance):
		instance.delete()
	

class ProjectMembersByProject(viewsets.ModelViewSet):
	serializer_class = ProjectMemberSerializer
	def get_permissions(self):
		if self.action in ['list','retrieve']:
			return  [IsAuthenticated()]
		return [Or(IsGrcAdmin,IsProjectAdmin,IsProjectManager,IsAdminUser())]

	def get_queryset(self):
		project_id = self.kwargs.get('project_id')
		return ProjectMember.objects.filter(project_id=project_id)

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
			
	# @swagger_auto_schema(
	# 	operation_description="Add a new member to a project",
	# 	request_body=ProjectMemberSerializer,
	# 	responses={
	# 		201: ProjectMemberSerializer,
	# 		400: openapi.Response(description="Bad Request", examples={
	# 			'application/json': {'detail': 'Invalid data'}
	# 		})
	# 	},
	# 	tags=["Project Members"],
	# 	operation_summary="Add Project Member"
	# )
	# def post(self, request, project_id):
	# 	data = request.data.copy()
	# 	data['project'] = project_id
	# 	serializer = ProjectMemberSerializer(data=data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return Response(serializer.data, status=status.HTTP_201_CREATED)
	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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



class TenantEvidenceModelViewSet(viewsets.ModelViewSet):
	queryset = Evidence.objects.all()
	serializer_class = EvidenceSerializer
	pagination_class = None
	filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)

	filterset_class = EvidenceFilterSet

	def get_queryset(self):
		return Evidence.objects.filter(
			tenant_id=self.kwargs.get('tenant_id')
		)

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		response_data = {
				'results': serializer.data
		}
		return Response(response_data)

@api_view(
		["GET"]
)
@permission_classes([])
def normative_reference_view(request, project_id):
	clauses = ProjectClause.objects.filter(project_id=project_id)
	serializer = NormativeReferencesSerializer(clauses, many=True)
	return Response(serializer.data)

class CommentByProjectModelViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by("-pk")
	serializer_class = CommentSerializer

	def get_queryset(self):
		project_id = self.kwargs.get('project_id')
		return Comment.objects.filter(project_id=project_id)

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
  
class CommentByProjectTaskModelViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by("-pk")
	serializer_class = CommentSerializer

	def get_queryset(self):
		# project_id = self.kwargs.get('project_id')
		task_id = self.kwargs.get('task_id')
		return Comment.objects.filter( task_id=task_id)

	def perform_create(self, serializer):
		# project_id = self.kwargs.get('project_id')
		# project = Project.objects.get(id=project_id)
		task_id = self.kwargs.get('task_id')
		task = ProjectTask.objects.get(id=task_id)
		serializer.save( task=task)

	def perform_update(self, serializer):
		# project_id = self.kwargs.get('project_id')
		# project = Project.objects.get(id=project_id)
		task_id = self.kwargs.get('task_id')
		task = ProjectTask.objects.get(id=task_id)
		serializer.save( task=task)

	def perform_destroy(self, instance):
		instance.delete()
  
class NoteByProjectTaskModelViewSet(viewsets.ModelViewSet):
	queryset = Note.objects.all().order_by("-pk")
	serializer_class = NoteSerializer

	def get_queryset(self):
		# project_id = self.kwargs.get('project_id')
		task_id = self.kwargs.get('task_id')
		return Note.objects.filter(task_id=task_id)

	def perform_create(self, serializer):
		# project_id = self.kwargs.get('project_id')
		# project = Project.objects.get(id=project_id)
		task_id = self.kwargs.get('task_id')
		task = ProjectTask.objects.get(id=task_id)
		serializer.save(task=task)

	def perform_update(self, serializer):
		# project_id = self.kwargs.get('project_id')
		# project = Project.objects.get(id=project_id)
		task_id = self.kwargs.get('task_id')
		task = ProjectTask.objects.get(id=task_id)
		serializer.save(task=task)

	def perform_destroy(self, instance):
		instance.delete()

class EvidenceByProjectTaskModelViewSet(viewsets.ModelViewSet):
	serializer_class = EvidenceSerializer

	def get_queryset(self):
		task_id = self.kwargs.get('task_id')
		if task_id:
			return Evidence.objects.filter(task__id=task_id)  # Filter by task ID in ManyToManyField
		return Evidence.objects.none()  # Return an empty queryset if `task_id` is not provided

	def perform_create(self, serializer):
		task_id = self.kwargs.get('task_id')
		if task_id:
			task = ProjectTask.objects.get(id=task_id)  # Fetch the task instance
			evidence = serializer.save()  # Save the Evidence instance

			# Add the task to the ManyToManyField
			evidence.task.add(task)

			# Handling uploaded files
			files = self.request.FILES.getlist('files')
			for file in files:
				evidence_file = EvidenceFile.objects.create(file=file)
				evidence.files.add(evidence_file)  # Add each file to the ManyToManyField

	def perform_update(self, serializer):
		task_id = self.kwargs.get('task_id')
		if task_id:
			task = ProjectTask.objects.get(id=task_id)  # Fetch the task instance
			evidence = serializer.save()  # Save the updated Evidence instance

			# Add the task to the ManyToManyField (ensure it is included)
			evidence.task.add(task)

			# Handling uploaded files during update
			files = self.request.FILES.getlist('files')
			if files:
				# Optionally clear existing files if needed
				# evidence.files.clear()  
				for file in files:
					evidence_file = EvidenceFile.objects.create(file=file)
					evidence.files.add(evidence_file)

	def perform_destroy(self, instance):
		instance.delete()


class ContextFileByProjectTaskModelViewSet(viewsets.ModelViewSet):
	
	serializer_class = ContextFileSerializer

	def get_queryset(self):
		project_id = self.kwargs.get('project_id')
		task_id = self.kwargs.get('task_id')
		
		return ContextFile.objects.filter(project__id=project_id, task__id=task_id)
	def perform_create(self, serializer):
		try:
			project_id = self.kwargs.get('project_id')
			project = Project.objects.get(id=project_id)
			task_id = self.kwargs.get('task_id')
			task = ProjectTask.objects.get(id=task_id)
			uploaded_file = self.request.FILES.get('file')
			serializer.save(file=uploaded_file, project=project, task=task)
			
		except Exception as e:
			print(f"Error: {e}")
			return Response({"error": "Error creating context file"}, status=status.HTTP_400_BAD_REQUEST)
		   

	def perform_update(self, serializer):
		# Retrieve project and task based on kwargs
		project_id = self.kwargs.get('project_id')
		project = Project.objects.get(id=project_id)
		task_id = self.kwargs.get('task_id')
		task = ProjectTask.objects.get(id=task_id)
		uploaded_file = self.request.FILES.get('file')
		serializer.save(project=project, task=task, file=uploaded_file)
		



	def perform_destroy(self, instance):
		# Delete the instance
		instance.delete()

  
class RemoveEvidenceFileView(APIView):
	
	def delete(self, request, evidence_id, file_id):

		evidence = Evidence.objects.get(id=evidence_id)
		evidence_file = EvidenceFile.objects.get(id=file_id)
		
		
		# Check if the file is associated with the evidence
		if not evidence.files.filter(id=file_id).exists():
			return Response(
				{"detail": "File not associated with this evidence."},
				status=status.HTTP_400_BAD_REQUEST
			)

		# Remove the file from the evidence's ManyToMany relationship
		evidence.files.remove(evidence_file)
				# Delete the file from the filesystem
		if evidence_file.file:  # Assuming the file field is named 'file'
			file_path = evidence_file.file.path  # Get the file path
			
			if os.path.isfile(file_path):
				os.remove(file_path)  
		evidence_file.delete()
		
		return Response(
			{"detail": "File removed from the evidence successfully."},
			status=status.HTTP_204_NO_CONTENT
		)
		
class ProjectScratchpadModelViewSet(viewsets.ModelViewSet):
	serializer_class = ProjectScratchpadSerializer

	
	def get_queryset(self):
		project_id = self.kwargs.get('project_id')
		return ProjectScratchpad.objects.filter(project_id=project_id)
	
	def list(self, request, *args, **kwargs):
			project_id = self.kwargs.get('project_id')
			project = Project.objects.get(id=project_id)
			if not project.can_read_scratchpad:
					raise PermissionDenied("Cannot read scratchpad.")
			return super().list(request, *args, **kwargs)


	def retrieve(self, request, *args, **kwargs):
			project_id = self.kwargs.get('project_id')
			project = Project.objects.get(id=project_id)
			if not project.can_read_scratchpad:
					raise PermissionDenied("Cannot read scratchpad.")
			return super().retrieve(request, *args, **kwargs)

	# def create(self, serializer):
	# 	return Response({"detail": "Cannot create new scratchpad."}, status=status.HTTP_403_FORBIDDEN)

	def perform_update(self, serializer):
		project_id = self.kwargs.get('project_id')
		project = Project.objects.get(id=project_id)
		if not project.can_write_scratchpad:
			raise PermissionDenied("Cannot write scratchpad.")
		# project_scratchpad = ProjectScratchpad.objects.get(project_id=project_id)
		serializer.save()

	def perform_partial_update(self, serializer):
			project_id = self.kwargs.get('project_id')
			project = Project.objects.get(id=project_id)
			if not project.can_write_scratchpad:
					raise PermissionDenied("Cannot write scratchpad.")
			serializer.save()

class CommentByProjectControlModelViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by("-pk")
	serializer_class = CommentSerializer

	def get_queryset(self):
		control_id = self.kwargs.get('control_id')
		return Comment.objects.filter( control_id=control_id)

	def perform_create(self, serializer):

		control_id = self.kwargs.get('control_id')
		control = ProjectControl.objects.get(id=control_id)
		serializer.save( control=control)

	def perform_update(self, serializer):

		control_id = self.kwargs.get('control_id')
		control = ProjectControl.objects.get(id=control_id)
		serializer.save( control=control)

	def perform_destroy(self, instance):
		instance.delete()
  
class NoteByProjectControlModelViewSet(viewsets.ModelViewSet):
	queryset = Note.objects.all().order_by("-pk")
	serializer_class = NoteSerializer

	def get_queryset(self):
		
		control_id = self.kwargs.get('control_id')
		return Note.objects.filter(control_id=control_id)

	def perform_create(self, serializer):

		control_id = self.kwargs.get('control_id')
		control = ProjectControl.objects.get(id=control_id)
		serializer.save(control=control)

	def perform_update(self, serializer):

		control_id = self.kwargs.get('control_id')
		control = ProjectControl.objects.get(id=control_id)
		serializer.save(control=control)

	def perform_destroy(self, instance):
		instance.delete()
  
class AuditorFeedbackByProjectControlModelViewSet(viewsets.ModelViewSet):
	queryset = AuditorFeedback.objects.all().order_by("-pk")
	serializer_class = AuditorFeedbackSerializer

	def get_queryset(self):
		
		control_id = self.kwargs.get('control_id')
		return AuditorFeedback.objects.filter(control_id=control_id)

	def perform_create(self, serializer):

		control_id = self.kwargs.get('control_id')
		control = ProjectControl.objects.get(id=control_id)
		serializer.save(control=control)

	def perform_update(self, serializer):

		control_id = self.kwargs.get('control_id')
		control = ProjectControl.objects.get(id=control_id)
		serializer.save(control=control)

	def perform_destroy(self, instance):
		instance.delete()
  
class ProjectStatusView(APIView):
	permission_classes = [IsAuthenticated]


	def get(self, request, project_id):
			project = Project.objects.get(id=project_id)
			tasks = ProjectTask.objects.filter(project=project)

			# Calculate completion percentage
			total_tasks = tasks.count()
			completed_tasks = tasks.filter(is_completed=True).count()
			completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

			# Calculate implementation average
			implementation_average = tasks.aggregate(models.Avg('completion'))['completion__avg'] or 0

			# Calculate review progress
			reviewed_tasks = tasks.filter(is_audited=True).count()
			review_progress = (reviewed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

			# Calculate evidence progress
			evidence_required_tasks = tasks.filter(evidence_required=True)
			total_evidence_required_tasks = evidence_required_tasks.count()
			evidence_available_tasks = evidence_required_tasks.filter(evidence_provided=100).count()
			# evidence_progress = evidence_required_tasks.aggregate(models.Avg('evidence_provided'))['evidence_provided__avg'] or 0
			evidence_progress = (evidence_available_tasks / total_evidence_required_tasks) * 100 if total_evidence_required_tasks > 0 else 0

			# Prepare response data
			data = {
					'completion_percentage': completion_percentage,
					'implementation_average': implementation_average,
					'review_progress': review_progress,
					'evidence_progress': evidence_progress
			}

			serializer = ProjectStatusSerializer(data=data)
			serializer.is_valid(raise_exception=True)
			return Response(serializer.data)

class ProjectEvidenceView(APIView):
	permission_classes = [IsAuthenticated]
	
	def get(self, request, project_id):
		# Retrieve all evidence related to the given project ID
		evidence_list = Evidence.objects.filter(task__project__id=project_id).distinct()
		
		
		# Serialize the evidence data
		serializer = EvidenceSerializer(evidence_list, many=True)
		
				# Construct the standard response
		# Construct the standard response with count
		response = {
			"success": True,
			"message": "Evidence retrieved successfully",
			"count": evidence_list.count(),
			"results": serializer.data,
		}
		# Return the serialized data as a response
		return Response(response)
	
class AuditorSummaryView(APIView):
	def get(self, request, project_id):
		data = {
			'project_id':project_id
		}
		serializer=AuditorSummarySerrializer(data=data,context={'project_id':project_id})
		serializer.is_valid(raise_exception=True)
		return Response(serializer.data)


class ControlAddToProjectView(APIView):

	@swagger_auto_schema(
        request_body=ControlAddToProjectSerializer,
        responses={
            200: openapi.Response(
                description="Successs",
                examples={
                    "application/json": {
                        "response": "success",
                        "msg": "Successfully added"
                    }
                }
            ),
            404: openapi.Response(
                description="Error: Not Found",
                examples={
                    "application/json": {
                        "response": "error",
                        "msg": "Not found"
                    }
                }
            ),
        },
    )
	def post(self, request, *args, **kwargs):
		control_id = request.data.get('control_id')
		project_id = request.data.get('project_id')
		try:
			control = ProjectControl.objects.get(id=control_id)
			project = Project.objects.get(id=project_id)
			control.project.add(project)
			return Response({
				"response": "success",
				"msg": "Successfully added"
			}, status=status.HTTP_200_OK)
		except:
			return Response({
				"response": "error",
				"msg": "Not found"
			}, status=404)


class PolicyAddToProjectView(APIView):

	@swagger_auto_schema(
        request_body=PolicyAddToProjectSerializer,
        responses={
            200: openapi.Response(
                description="Successs",
                examples={
                    "application/json": {
                        "response": "success",
                        "msg": "Successfully added"
                    }
                }
            ),
            404: openapi.Response(
                description="Error: Not Found",
                examples={
                    "application/json": {
                        "response": "error",
                        "msg": "Not found"
                    }
                }
            ),
        },
    )
	def post(self, request, *args, **kwargs):
		policy_id = request.data.get('policy_id')
		project_id = request.data.get('project_id')
		try:
			policy = TenantPolicy.objects.get(id=policy_id)
			project = Project.objects.get(id=project_id)
			policy.project.add(project)
			return Response({
				"response": "success",
				"msg": "Successfully added"
			}, status=status.HTTP_200_OK)
		except:
			return Response({
				"response": "error",
				"msg": "Not found"
			}, status=404)


class EvidenceAddToProjectTaskView(APIView):

	@swagger_auto_schema(
        request_body=EvidenceAddToProjectTaskSerializer,
        responses={
            200: openapi.Response(
                description="Successs",
                examples={
                    "application/json": {
                        "response": "success",
                        "msg": "Successfully added"
                    }
                }
            ),
            404: openapi.Response(
                description="Error: Not Found",
                examples={
                    "application/json": {
                        "response": "error",
                        "msg": "Not found"
                    }
                }
            ),
        },
    )
	def post(self, request, *args, **kwargs):
		evidence_id = request.data.get('evidence_id')
		projecttask_id = request.data.get('projecttask_id')
		try:
			evidence = Evidence.objects.get(id=evidence_id)
			project_task = ProjectTask.objects.get(id=projecttask_id)
			evidence.task.add(project_task)
			return Response({
				"response": "success",
				"msg": "Successfully added"
			}, status=status.HTTP_200_OK)
		except:
			return Response({
				"response": "error",
				"msg": "Not found"
			}, status=404)


class ProjectByTenantView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tenant_id):
        try:
            projects = Project.objects.filter(tenant_id=tenant_id)
            if projects.exists():
				# print(projects)
                serializer = ProjectSerializer(projects, many=True)
                return Response({"results":serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"results": []},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"response": "error", "message": f"An unexpected error occurred. Please try again later.{e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
