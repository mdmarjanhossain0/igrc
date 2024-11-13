from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FrameworkModelViewSet,
    TaskModelViewSet,
    ClauseModelViewSet,
    PolicyModelViewSet,
    ControlModelViewSet,
    ProjectModelViewSet,
    ProjectMemberModelViewSet,
    ProjectTaskModelViewSet,
    ProjectClauseModelViewSet,
    TenantPolicyModelViewSet,
    ProjectControlModelViewSet
)

app_name='app_api'

router = DefaultRouter()
router.register(r'frameworks', FrameworkModelViewSet)
router.register(r'tasks', TaskModelViewSet)
router.register(r'clauses', ClauseModelViewSet)
router.register(r'policies', PolicyModelViewSet)
router.register(r'controls', ControlModelViewSet)
router.register(r'projects', ProjectModelViewSet)
router.register(r'project-members', ProjectMemberModelViewSet)
router.register(r'project-tasks', ProjectTaskModelViewSet)
router.register(r'project-clauses', ProjectClauseModelViewSet)
router.register(r'tenant-policies', TenantPolicyModelViewSet)
router.register(r'project-controls', ProjectControlModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
