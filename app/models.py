from django.db import models
from mysite.settings import DEFAULT_AUTO_FIELD
from account.models import Account

# from django_ckeditor_5.fields import CKEditor5Field

from django.db.models.signals import post_save
from django.dispatch import receiver

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Framework(BaseModel):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    reference_link=models.CharField(max_length=255, null=True,blank=True)

    def __str__(self):
        return self.title


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


    def __str__(self):
        return self.title
    
class SubControl(BaseModel):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    control = models.ForeignKey(Control, on_delete=models.CASCADE)
    
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=True,blank=True)


    def __str__(self):
        return self.title





class Tenant(BaseModel):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    contact_email=models.EmailField(null=False,blank=False)
    owner=models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Project(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    framework = models.ForeignKey(Framework, on_delete=models.SET_NULL, null=True, blank=True)

    framework_title = models.CharField(max_length=255)
    framework_description=models.TextField(null=False,blank=False)

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    description=models.TextField(null=True,blank=True)


class ProjectMember(BaseModel):

    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('external_auditor', 'Auditor(External)'),
        ('internal_auditor', 'Auditor(Internal)'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(Account, blank=False, on_delete=models.CASCADE)
    role=models.CharField(max_length=255, choices=ROLE_CHOICES ,default="viewer")

    def __str__(self):
        return self.member.username



class ProjectTask(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

    assigned_member = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    deadline = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)



class ProjectClause(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    clause = models.ForeignKey(Clause, on_delete=models.SET_NULL, null=True, blank=True)


class TenantPolicy(BaseModel):
    project = models.ManyToManyField(Project, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

class ProjectControl(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    control = models.ForeignKey(Control, on_delete=models.SET_NULL, null=True, blank=True)

class ProjectSubControl(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sub_control = models.ForeignKey(SubControl, on_delete=models.SET_NULL, null=True, blank=True)
    project_control = models.ForeignKey(ProjectControl, on_delete=models.CASCADE)

class Evidence(BaseModel):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    policy = models.ForeignKey(TenantPolicy, on_delete=models.SET_NULL, null=True, blank=True)
    control = models.ForeignKey(ProjectControl, on_delete=models.SET_NULL, null=True, blank=True)
    sub_control = models.ForeignKey(ProjectSubControl, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=255, null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    file = models.FileField(upload_to='evidence/', null=True, blank=True)




@receiver(post_save, sender=Project)
def created_project_receiver(sender, instance=None, created=False, **kwargs):
    if created:
        for item in instance.framework.task_set.all():
            ProjectTask.objects.create(
                project=instance,
                task=item
            )
        for item in instance.framework.clause_set.all():
            ProjectClause.objects.create(
                project=instance,
                clause=item
            )
        for item in instance.framework.policy_set.all():
            TenantPolicy.objects.create(
                project=instance
            )
        for item in instance.framework.control_set.all():
            ProjectControl.objects.create(
                project=instance,
                control=item
            )
