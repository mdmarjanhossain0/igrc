from rest_framework.permissions import BasePermission
from app.models import ProjectMember
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
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Get the project ID from the view's kwargs
        project_id = view.kwargs.get('pk')
        
        # Check if the user is an admin in the specific project
        return ProjectMember.objects.filter(
            project_id=project_id,
            member=request.user,
            role='Admin'
        ).exists()
    
class IsProjectManager(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Get the project ID from the view's kwargs
        project_id = view.kwargs.get('pk')
        
        # Check if the user is an admin in the specific project
        return ProjectMember.objects.filter(
            project_id=project_id,
            member=request.user,
            role='Manager'
        ).exists()

class IsGrcAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user.is_authenticated and request.user.role== Account.ADMIN


