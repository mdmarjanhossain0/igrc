from django.db import models
from mysite.settings import DEFAULT_AUTO_FIELD
from account.models import Account, Audit

from django.core.validators import MinValueValidator, MaxValueValidator
# from django_ckeditor_5.fields import CKEditor5Field

from django.db.models.signals import post_save
from django.dispatch import receiver

from grc_config.models import (
    BaseModel,
    StatusDB
)

class Framework(BaseModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    reference_link=models.CharField(max_length=255, null=True,blank=True)

    def __str__(self):
        return self.name

class Task(BaseModel):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    
    id=models.AutoField(primary_key=True,)
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title
    
class Clause(BaseModel):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=True,blank=True)

class Policy(BaseModel):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=True,blank=True)
    content=models.TextField(null=False,blank=False)

class Control(BaseModel):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=True,blank=True)

    refcode=models.CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return self.title
    
class SubControl(BaseModel):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    control = models.ForeignKey(Control, related_name="subcontrols",on_delete=models.CASCADE)
    
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=True,blank=True)

    refcode=models.CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return self.title


class Tenant(BaseModel):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    contact_email=models.EmailField(null=False,blank=False)
    owner=models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False, related_name="tenant_owner")


    def __str__(self):
        return self.title

class Project(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    framework = models.ForeignKey(Framework, on_delete=models.SET_NULL, null=True, blank=True)

    framework_name = models.CharField(max_length=255, null=True,blank=True)
    framework_description=models.TextField(null=True,blank=True)


    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)
    status = models.ForeignKey(StatusDB, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    description=models.TextField(null=True,blank=True)
    is_auditable = models.BooleanField(default=False)

    can_read_scratchpad=models.BooleanField(default=True)
    can_write_scratchpad=models.BooleanField(default=True)
    can_read_comments=models.BooleanField(default=True)
    can_write_comments=models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.framework_name and self.framework:
            self.framework_name = self.framework.name
        if not self.framework_description and self.framework:
            self.framework_description = self.framework.description
        


        super(Project, self).save(*args, **kwargs)

class ProjectMember(BaseModel):

    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('Editor', 'Editor'),
        ('Admin', 'Admin'),
        ('Manager','Manager'),
        ('external_auditor', 'Auditor(External)'),
        ('internal_auditor', 'Auditor(Internal)'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(Account, blank=False, on_delete=models.CASCADE)
    role=models.CharField(max_length=255, choices=ROLE_CHOICES ,default="viewer")
    
    all_clause = models.BooleanField(default=True)
    clauses = models.ManyToManyField('ProjectClause', blank=True)
    all_policy = models.BooleanField(default=True)
    policies = models.ManyToManyField('TenantPolicy', blank=True)
    all_control = models.BooleanField(default=True)
    controls = models.ManyToManyField("ProjectControl", blank=True)
    all_sub_control = models.BooleanField(default=True)
    sub_controls = models.ManyToManyField("ProjectSubControl", blank=True)
    all_task = models.BooleanField(default=True)
    tasks=models.ManyToManyField("ProjectTask", blank=True)
    def __str__(self):
        return self.member.username

@receiver(post_save, sender=ProjectMember)
def assign_all_related_fields(sender, instance, created, **kwargs):
    if created:
        if instance.all_clause:
            instance.clauses.set(ProjectClause.objects.filter(project=instance.project))
        if instance.all_policy:
            instance.policies.set(TenantPolicy.objects.filter(project=instance.project))
        if instance.all_control:
            instance.controls.set(ProjectControl.objects.filter(project=instance.project))
        if instance.all_sub_control:
            instance.sub_controls.set(ProjectSubControl.objects.filter(project=instance.project))
        if instance.all_task:
            instance.tasks.set(ProjectTask.objects.filter(project=instance.project))

class ProjectTask(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

    title=models.CharField(max_length=255, null=True,blank=True)
    description=models.TextField(null=True, blank=True)
    status = models.ForeignKey(StatusDB, on_delete=models.SET_NULL, null=True, blank=True)
    
    # assigned_member = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    deadline = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)


class ProjectClause(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    clause = models.ForeignKey(Clause, on_delete=models.SET_NULL, null=True, blank=True)

    title=models.CharField(max_length=255, null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    

class TenantPolicy(BaseModel):
    project = models.ManyToManyField(Project, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    label = models.CharField(max_length=255, null=True, blank=True)
    refcode=models.CharField(max_length=32, null=False, blank=False)


class ProjectControl(BaseModel):
    status_choices=[
        ("not started","not started"),
        ("completed","completed")
    ]
    EASY = "Easy"
    MODARATE = "Moderate"
    HARD = "Hard"
    DIFFICULTIES = [
        (EASY, EASY),
        (MODARATE, MODARATE),
        (HARD, HARD),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    control = models.ForeignKey(Control, on_delete=models.SET_NULL, null=True, blank=True)

    title=models.CharField(max_length=255, null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.CharField(max_length=255, default="not started", choices=status_choices)
    refcode=models.CharField(max_length=32, null=False, blank=False)
    implementation_context=models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    sub_category =  models.TextField(null=True, blank=True)
    system_level = models.BooleanField(default=True)
    implementation_difficulty = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)
    collaboration_difficulty = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)

    def average_completion(self):
        avg_completion=ProjectSubControl.objects.filter(project_control=self).aggregate(models.Avg('completion'))
        return avg_completion['completion__avg'] or self.completion

class ProjectSubControl(BaseModel):
    
    status_choices=[
        ("not implemented","not implemented"),
        ("partially implemented","partially implemented"),
        ("fully implemented","fully implemented"),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sub_control = models.ForeignKey(SubControl, on_delete=models.SET_NULL, null=True, blank=True)
    project_control = models.ForeignKey(ProjectControl, on_delete=models.CASCADE)
    owner=models.ForeignKey(Account, on_delete=models.SET_NULL,null=True, blank=True, related_name="subcontrol_owner")
    operator=models.ForeignKey(Account, on_delete=models.SET_NULL,null=True, blank=True, related_name="subcontrol_operator")

    title=models.CharField(max_length=255, null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    applicable = models.BooleanField(default=True)
    refcode=models.CharField(max_length=32, null=False, blank=False)
    implementation_context=models.TextField(null=True, blank=True)
    mitigation = models.TextField(null=True, blank=True)

    completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    has_evidence= models.BooleanField(default=False)

    status= models.CharField(max_length=255, default="not implemented", choices=status_choices)
    
    #review
    #todo
    #category
    #subcategory

class EvidenceFile(BaseModel):
    file = models.FileField(upload_to='evidence/', null=True, blank=True)

class Evidence(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(ProjectTask, on_delete=models.SET_NULL, null=True, blank=True)
    clause = models.ForeignKey(ProjectClause, on_delete=models.SET_NULL, null=True, blank=True)
    policy = models.ForeignKey(TenantPolicy, on_delete=models.SET_NULL, null=True, blank=True)
    control = models.ForeignKey(ProjectControl, on_delete=models.SET_NULL, null=True, blank=True)
    sub_control = models.ForeignKey(ProjectSubControl, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=255, null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    files = models.ManyToManyField(EvidenceFile, blank=True)
    is_complete = models.BooleanField(default=False)

class Comment(BaseModel):
    policy = models.ForeignKey(TenantPolicy, on_delete=models.SET_NULL, null=True, blank=True)
    control = models.ForeignKey(ProjectControl, on_delete=models.SET_NULL, null=True, blank=True)
    sub_control = models.ForeignKey(ProjectSubControl, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    audit = models.ForeignKey(Audit, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)

class Note(BaseModel):
    policy = models.ForeignKey(TenantPolicy, on_delete=models.SET_NULL, null=True, blank=True)
    control = models.ForeignKey(ProjectControl, on_delete=models.SET_NULL, null=True, blank=True)
    sub_control = models.ForeignKey(ProjectSubControl, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    audit = models.ForeignKey(Audit, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)

class AuditorFeedback(BaseModel):
    status_choices=[
        ("not started","not started"),
        ("infosec: in progress","infosec: in progress"),
        ("infosec: ready for auditor","infosec: ready for auditor"),
        ("action required","action required"),
        ("completed", "completed")
    ]
    policy = models.ForeignKey(TenantPolicy, on_delete=models.SET_NULL, null=True, blank=True)
    control = models.ForeignKey(ProjectControl, on_delete=models.SET_NULL, null=True, blank=True)
    sub_control = models.ForeignKey(ProjectSubControl, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    status=models.CharField(max_length=255, choices=status_choices)
    auditor_note=models.TextField(null=True, blank=True)
    title=models.CharField(max_length=255)
    auditor_feedback = models.TextField(null=True, blank=True)
    infosec_feedback = models.TextField(null=True, blank=True)

    infosec_completed=models.BooleanField(default=False)
    auditor_completed=models.BooleanField(default=False)

    created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)


@receiver(post_save, sender=Project)
def created_project_receiver(sender, instance=None, created=False, **kwargs):
    if created:
        # instance.framework_name = instance.framework.name
        # instance.framework_description = instance.framework.description
        if instance.framework:
            for item in instance.framework.task_set.all():
                ProjectTask.objects.create(
                    project=instance,
                    task=item,
                    title=item.title,
                    description=item.description
                )
            for item in instance.framework.clause_set.all():
                ProjectClause.objects.create(
                    project=instance,
                    clause=item,
                    title=item.title,
                    description=item.description
                )
            # for item in instance.framework.policy_set.all():
                # tp = TenantPolicy(
                #     title=item.title,
                #     description=item.description,
                #     content=item.content
                # )
                # tp.save()
                
                # tp.project.set([item.pk])
                # tp.save()
                # pass


            for item in instance.framework.control_set.all():
                ProjectControl.objects.create(
                    project=instance,
                    control=item,
                    refcode=item.refcode,
                    
                )

            for item in instance.framework.subcontrol_set.all():
                ProjectSubControl.objects.create(
                    project=instance,
                    sub_control=item,
                    project_control=item.control.projectcontrol_set.first(),
                    title=item.title,
                    description=item.description,
                    refcode=item.refcode
                )
