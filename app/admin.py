from django.contrib import admin
from app.models import(
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

# Register your models here.
admin.site.register(Framework)
admin.site.register(Task)
admin.site.register(Clause)
admin.site.register(Policy)
admin.site.register(Control)

admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(ProjectTask)
admin.site.register(ProjectClause)
admin.site.register(TenantPolicy)
admin.site.register(ProjectControl)
