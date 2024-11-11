from django.db import models
from mysite.settings import DEFAULT_AUTO_FIELD
from account.models import Account

class Framework(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    reference_link=models.CharField(max_length=255, null=True,blank=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    pass

class Task(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    
    id=models.AutoField(primary_key=True,)
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=True,blank=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    pass

class Clause(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    pass

class Policy(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    
    pass

class Control(models.Model):
    
    # framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=True,blank=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    pass






class Tenant(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255, null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    contact_email=models.EmailField(null=False,blank=False)
    owner=models.ForeignKey(Account, on_delete=models.CASCADE)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    pass

class Project(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    description=models.TextField(null=True,blank=True)


    pass

class ProjectMember(models.Model):

    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('external_auditor', 'Auditor(External)'),
        ('internal_auditor', 'Auditor(Internal)'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(Account, blank=False, on_delete=models.CASCADE)
    role=models.CharField(max_length=255, choices=ROLE_CHOICES ,default="viewer")

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.member.username
    pass


class ProjectTask(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    assigned_member = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    deadline = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    pass

class ProjectClause(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pass

class TenantPolicy(models.Model):
    project = models.ManyToManyField(Project, blank=True)
    pass

class ProjectControl(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pass

class Evidance(models.Model):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    control = models.ForeignKey(ProjectControl, on_delete=models.CASCADE)
    pass
