from rest_framework import serializers
from app.models import (Clause, Control, Evidence, EvidenceFile, Framework, Policy, Project,
    ProjectClause, ProjectControl, ProjectMember, ProjectSubControl, ProjectTask, SubControl, Task,
    Tenant, TenantPolicy)


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

class SubControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubControl
        fields = '__all__'

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tenant
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
    completion=serializers.SerializerMethodField()
    class Meta:
        model = ProjectControl
        fields = '__all__'
    
    def get_completion(self, obj):
        return obj.average_completion()

class ProjectSubControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSubControl
        fields = '__all__'

class EvidenceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceFile
        fields = '__all__'
class EvidenceSerializer(serializers.ModelSerializer):
    files = EvidenceFileSerializer(many=True, read_only=True)

    class Meta:
        model = Evidence
        fields = '__all__'

# class ClauseByProjectSerializer(serializers.ModelSerializer):
#     project_clauses=serializers.SerializerMethodField()
#     class Meta:
#         model = Clause
#         fields = '__all__'

class ControlWithSubControlSerializer(serializers.ModelSerializer):
    subcontrols=SubControlSerializer(many=True, read_only=True)
    evidences=serializers.SerializerMethodField()
    class Meta:
        model = Control
        fields = '__all__'
    
    # def get_subcontrols(self,obj):
    #     subcontrols=SubControl.objects.filter(control=obj)
    #     return SubControlSerializer(subcontrols, many=True).data

    def get_evidences(self, obj):
        evidences=Evidence.objects.filter(control__control=obj)
        return EvidenceSerializer(evidences,many=True).data
