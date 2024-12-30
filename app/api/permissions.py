from rest_framework.permissions import BasePermission
from app.models import Project, ProjectMember, Tenant
from account.models import Account



class Or(BasePermission):
    def __init__(self, *perms):
        self.perms = perms

    def has_permission(self, request, view):
        return any(perm().has_permission(request, view) for perm in self.perms)

    def has_object_permission(self, request, view, obj):
        return any(perm().has_object_permission(request, view, obj) for perm in self.perms)

class IsProjectAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        project_id = view.kwargs.get('project_id')
        
        return ProjectMember.objects.filter(
            project_id=project_id,
            member=request.user,
            role='Admin'
        ).exists()
    
class IsTenantOwner(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        tenant_id = request.data.get('tenant')

        return Tenant.objects.filter(
            id=tenant_id,
            owner=request.user
        ).exists()
class IsProjectManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        project_id = view.kwargs.get('project_id')
        print(project_id)
        exists=ProjectMember.objects.filter(
            project_id=project_id,
            member=request.user,
            role='Manager'
        ).exists()
        print(exists)
        return exists

class IsProjectViewer(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        project_id = view.kwargs.get('project_id')
    
        return ProjectMember.objects.filter(
            project_id=project_id,
            member=request.user,
            role='Viewer'
        ).exists()
    
class IsGrcAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role== Account.ADMIN
