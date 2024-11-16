from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ClauseModelViewSet, ControlModelViewSet, FrameworkModelViewSet,
    PolicyModelViewSet, ProjectClauseModelViewSet, ProjectControlModelViewSet,
    ProjectMemberModelViewSet, ProjectModelViewSet, ProjectSubControlModelViewSet,
    ProjectTaskModelViewSet, SubControlModelViewSet, TaskModelViewSet, TenantModelViewSet,
    TenantPolicyModelViewSet)

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
router.register(r'project-controls', ProjectControlModelViewSet)
router.register(r'project-subcontrols', ProjectSubControlModelViewSet)

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

]
