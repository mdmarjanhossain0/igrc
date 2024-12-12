from rest_framework import serializers
from app.models import (AuditorFeedback, Clause, Comment, Control, Evidence, EvidenceFile,
    Framework, Note, Policy, Project, ProjectClause, ProjectControl, ProjectMember,
    ProjectSubControl, ProjectTask, SubControl, Task, Tenant, TenantPolicy)
from django.db.models import Sum, Avg
from riskapp.api.serializers import RiskMitigationSerializer
from riskapp.models import RiskMitigation
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
    completion = serializers.SerializerMethodField("get_completion")
    implementation = serializers.SerializerMethodField("get_implementation")
    toatl_clauses = serializers.SerializerMethodField("get_total_clauses")
    toatl_policies = serializers.SerializerMethodField("get_total_policies")
    toatl_controls = serializers.SerializerMethodField("get_total_controls")
    total_evidences = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField("get_status")
    owner_name = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'

    def get_owner_name(self, obj):
        try:
            return obj.owner.username
        except:
            return None
        
    def get_status(self, obj):
        try:
            return obj.status.name
        except:
            return "In Progress"
    
    def get_total_clauses(self, obj):
        return obj.projectclause_set.all().count()
    
    def get_total_policies(self, obj):
        return obj.tenantpolicy_set.all().count()
    
    def get_total_controls(self, obj):
        return obj.projectcontrol_set.all().count()
    
    def get_completion(self, obj):
        avg_completion=ProjectClause.objects.filter(project=obj).aggregate(Avg('completion'))
        print(avg_completion)
        return avg_completion['completion__avg'] or 0
    
    def get_implementation(self, obj):
        controls = obj.projectcontrol_set.all()
        if len(controls) == 0:
            return 0
        else:
            sum = 0
            for item in controls:
                sum += item.average_completion()
            return sum / len(controls)
        
    def get_total_evidences(self, obj):
        objs = obj.evidence_set.all()
        sum = 0
        for item in objs:
            sum += 1 if item.is_complete else 0
        return sum / len(objs) if len(objs) > 0 else 1

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
    evidences = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    notes=serializers.SerializerMethodField()
    auditor_feedback=serializers.SerializerMethodField()
    class Meta:
        model = ProjectControl
        fields = '__all__'
    
    def get_completion(self, obj):
        return obj.average_completion()

    def get_notes(self,obj):
        return NoteSerializer(obj.note_set.all(), many=True).data
    
    def get_auditor_feedback(self,obj):
        return AuditorFeedbackSerializer(obj.auditorfeedback_set.all(), many=True).data
    
    def get_evidences(self, obj):
        return EvidenceSerializer(obj.evidence_set.all(), many=True).data
    def get_comments(self, obj):
        return CommentSerializer(obj.comment_set.all(), many=True).data

class ProjectSubControlSerializer(serializers.ModelSerializer):
    evidences = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    auditor_feedback = serializers.SerializerMethodField()

    mitigations=serializers.SerializerMethodField()
    class Meta:
        model = ProjectSubControl
        fields = '__all__'
    
    def get_mitigations(self,obj):
        control=obj.project_control
        print(control)
        risks=control.riskregister_set.all()
        mitigations = RiskMitigation.objects.filter(risk__in=risks)
        print(risks)
        print(mitigations)
        return RiskMitigationSerializer(mitigations, many=True).data
    
    def get_evidences(self, obj):
        return EvidenceSerializer(obj.evidence_set.all(), many=True).data
    def get_auditor_feedback(self, obj):
        print(obj.auditorfeedback_set.all())
        return AuditorFeedbackSerializer(obj.auditorfeedback_set.all(), many=True).data
    
    def get_comments(self, obj):
        return CommentSerializer(obj.comment_set.all(), many=True).data
    def get_notes(self, obj):
        return NoteSerializer(obj.note_set.all(), many=True).data

class EvidenceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceFile
        fields = '__all__'

class EvidenceSerializer(serializers.ModelSerializer):
    files = EvidenceFileSerializer(many=True, read_only=False)

    class Meta:
        model = Evidence
        fields = '__all__'

# class ClauseByProjectSerializer(serializers.ModelSerializer):
#     project_clauses=serializers.SerializerMethodField()
#     class Meta:
#         model = Clause
#         fields = '__all__'

class ControlWithSubControlSerializer(serializers.ModelSerializer):
    subcontrols=serializers.SerializerMethodField()
    evidences = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    completion=serializers.SerializerMethodField()
    evidences = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    notes=serializers.SerializerMethodField()
    auditor_feedback=serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    evidence_progress = serializers.SerializerMethodField()
    class Meta:
        model = ProjectControl
        fields = '__all__'
    
    def get_evidence_progress(self, obj):
        try:
            progress = 0
            total_evidences = obj.evidence_set.all().count()
            completed_evidences = obj.evidence_set.filter(is_complete=True).count()
            if total_evidences > 0:
                progress = completed_evidences / total_evidences * 100
            return progress
        except:
            return 0

    def get_review_count(self, obj):
        return obj.auditorfeedback_set.filter(status="completed").count()
    def get_completion(self, obj):
        return obj.average_completion()

    def get_notes(self,obj):
        return NoteSerializer(obj.note_set.all(), many=True).data
    
    def get_auditor_feedback(self,obj):
        return AuditorFeedbackSerializer(obj.auditorfeedback_set.all(), many=True).data
    
    def get_subcontrols(self,obj):
        subcontrols=SubControl.objects.filter(control=obj)

        subcontrols_data = SubControlSerializer(subcontrols, many=True).data
        for subcontrol in subcontrols_data:
            subcontrol_obj = SubControl.objects.get(id=subcontrol['id'])
            evidences = Evidence.objects.filter(sub_control__sub_control=subcontrol_obj)
            subcontrol['evidences'] = EvidenceSerializer(evidences, many=True).data
        return subcontrols_data
    
    def get_evidences(self, obj):
        return EvidenceSerializer(obj.evidence_set.all(), many=True).data
    def get_comments(self, obj):
        return CommentSerializer(obj.comment_set.all(), many=True).data
    def get_notes(self, obj):
        return NoteSerializer(obj.note_set.all(), many=True).data
    

class ProjectControlWithSubControlSerializer(serializers.ModelSerializer):
    subcontrols=serializers.SerializerMethodField()
    evidences = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    class Meta:
        model = ProjectControl
        fields = '__all__'
    
    def get_subcontrols(self,obj):
        subcontrols=ProjectSubControl.objects.filter(project_control=obj)
        return ProjectSubControlSerializer(subcontrols, many=True).data
    
    def get_evidences(self, obj):
        return EvidenceSerializer(obj.evidence_set.all(), many=True).data
    def get_comments(self, obj):
        return CommentSerializer(obj.comment_set.all(), many=True).data
    def get_notes(self, obj):
        return NoteSerializer(obj.note_set.all(), many=True).data

class AuditorFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditorFeedback
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
