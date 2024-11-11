from django.db import models

class Framework(models.Model):
    pass

class Task(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    pass

class Clause(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    pass

class Policy(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    pass

class Control(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    pass






class Tenant(models.Model):
    pass

class Project(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
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