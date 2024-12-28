from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AditorFeedBackViewSet, AuditorSummaryView, ClauseModelViewSet, ClausesByProjectView,
    CommentByProjectControlModelViewSet, CommentByProjectModelViewSet, CommentByProjectTaskModelViewSet,
    CommentViewSet, ContextFileByProjectTaskModelViewSet, ControlModelViewSet, ControlsByProjectView,
    ControlWithSubControlsByProjectView, EvidenceModelViewSet, FrameworkModelViewSet, normative_reference_view,
    PolicyModelViewSet, ProjectClauseModelViewSet, ProjectControlModelViewSet, ProjectMemberByProject,
    ProjectMemberModelViewSet, ProjectMembersByProject, ProjectModelViewSet, ProjectPoicyModelViewSet,
    ProjectScratchpadModelViewSet, ProjectSubControlModelViewSet, ProjectTaskModelViewSet, SubControlModelViewSet,
    SubControlsByProjectView, TaskModelViewSet, TasksByProjectView, TenantEvidenceModelViewSet, TenantModelViewSet,
    TenantPolicyModelViewSet, NoteViewSet, NoteByProjectTaskModelViewSet, EvidenceByProjectTaskModelViewSet,
    RemoveEvidenceFileView, NoteByProjectControlModelViewSet, ProjectStatusView,
    AuditorFeedbackByProjectControlModelViewSet, ProjectEvidenceView,
    ControlAddToProjectView
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

app_name='app_api'

router = DefaultRouter()
router.register(r'frameworks', FrameworkModelViewSet)
router.register(r'tasks', TaskModelViewSet)
router.register(r'clauses', ClauseModelViewSet)
router.register(r'policies', PolicyModelViewSet)
router.register(r'controls', ControlModelViewSet)
router.register(r'subcontrols', SubControlModelViewSet)
router.register(r'tenants', TenantModelViewSet)
router.register(r'projects', ProjectModelViewSet)
router.register(r'project-members', ProjectMemberModelViewSet)
router.register(r'project-tasks', ProjectTaskModelViewSet)
router.register(r'project-clauses', ProjectClauseModelViewSet)
router.register(r'tenant-policies', TenantPolicyModelViewSet)
router.register(r'project-controls/(?P<tenant_id>\d+)', ProjectControlModelViewSet)
router.register(r'project-subcontrols', ProjectSubControlModelViewSet)
router.register(r'evidence', EvidenceModelViewSet)
router.register(r'note', NoteViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'aditorfeedback', AditorFeedBackViewSet)


router.register(r'project/(?P<project_id>\d+)/clauses',ClausesByProjectView, basename='project-clauses')

router.register(r'project/(?P<project_id>\d+)/scratchpad',ProjectScratchpadModelViewSet, basename='project-scratchpad')
router.register(r'project/(?P<project_id>\d+)/policies',ProjectPoicyModelViewSet, basename='project-policy')
router.register(r'project/(?P<project_id>\d+)/controls',ControlsByProjectView, basename='project-controls')
router.register(r'project/(?P<project_id>\d+)/controls/(?P<control_id>\d+)/subcontrols', SubControlsByProjectView, basename='project-subcontrols')
router.register(r'project/(?P<project_id>\d+)/tasks', TasksByProjectView, basename='project-tasks')
router.register(r'project/(?P<project_id>\d+)/controls-with-subcontrols', ControlWithSubControlsByProjectView, basename='project-controls-with-subcontrols')
router.register(r'project/(?P<project_id>\d+)/members', ProjectMembersByProject, basename='project-members')
router.register(r'project/(?P<project_id>\d+)/comments', CommentByProjectModelViewSet, basename='project-comments'),
router.register(r'evidence_set/(?P<tenant_id>\d+)', TenantEvidenceModelViewSet, basename='evidence_set')

# Project Task
router.register(r'project/(?P<project_id>\d+)/task/(?P<task_id>\d+)/comments', CommentByProjectTaskModelViewSet, basename='project-task-comments'),
router.register(r'project/(?P<project_id>\d+)/task/(?P<task_id>\d+)/notes', NoteByProjectTaskModelViewSet, basename='project-task-notes'),
router.register(r'project/(?P<project_id>\d+)/task/(?P<task_id>\d+)/evidences', EvidenceByProjectTaskModelViewSet, basename='project-task-evidences'),
router.register(r'project/(?P<project_id>\d+)/task/(?P<task_id>\d+)/contexts', ContextFileByProjectTaskModelViewSet, basename='project-task-contexts'),

# Project Control
router.register(r'project/(?P<project_id>\d+)/control/(?P<control_id>\d+)/comments', CommentByProjectControlModelViewSet, basename='project-control-comments'),
router.register(r'project/(?P<project_id>\d+)/control/(?P<control_id>\d+)/notes', NoteByProjectControlModelViewSet, basename='project-control-notes'),
router.register(r'project/(?P<project_id>\d+)/control/(?P<control_id>\d+)/auditor-feedback', AuditorFeedbackByProjectControlModelViewSet, basename='project-control-auditor'),




schema_view=get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API for the app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@localhost"),
        license=openapi.License(name="BSD License"),

    ),
    public=True,
    permission_classes=[AllowAny],
)


urlpatterns = [
    path('', include(router.urls)),
    path("swagger", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    # path("project/<int:project_id>/clauses/", ClausesByProjectView.as_view(), name="project-clauses-by-project"),
    # path("project/<int:project_id>/controls/", ControlsByProjectView.as_view(), name="project-controls-by-project"),
    # path("project/<int:project_id>/controls-with-subcontrols/", ControlWithSubControlsByProjectView.as_view(), name="project-controls-with-subcontrols-by-project"),
    # path("project/<int:project_id>/tasks/", TasksByProjectView.as_view(), name="project-tasks-by-project"),


    # path("project/<int:project_id>/members/", ProjectMembersByProject.as_view(), name="project-members-by-project"),
    # path("project/<int:project_id>/members/<int:member_id>/", ProjectMemberByProject.as_view(), name="project-member-by-project"),

    path("project/<int:project_id>/normative_reference/", normative_reference_view, name="normative_reference_view"),
    path("normative_reference/<int:project_id>/", normative_reference_view, name="normative_reference_view"),
    path('project/task/evidence/<int:evidence_id>/file/<int:file_id>/remove/', RemoveEvidenceFileView.as_view(), name='remove-evidence-file'),
    path('project/<int:project_id>/status/', ProjectStatusView.as_view(), name='project-status'),
    path('project/<int:project_id>/evidences/', ProjectEvidenceView.as_view(), name='project-evidence'),
    
    path('project/<int:project_id>/auditor-summary/', AuditorSummaryView.as_view(), name='project-auditor-summary'),
    path("control_add_to_project/", ControlAddToProjectView.as_view(),)
]
