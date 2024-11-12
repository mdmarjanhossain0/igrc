from rest_framework import serializers
from app.models import (
    Framework,
    Task, 
    Clause, 
    Policy, 
    Control, 
    Project, 
    ProjectMember, 
    ProjectTask, 
    ProjectClause, 
    TenantPolicy, 
    ProjectControl
)
class FrameworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Framework
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clause
        fields = '__all__'

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'

class ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = '__all__'

class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = '__all__'

class ProjectClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectClause
        fields = '__all__'

class TenantPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantPolicy
        fields = '__all__'

class ProjectControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectControl
        fields = '__all__'
