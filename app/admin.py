from django.contrib import admin
from app.models import(
    Framework,
    Task,
    Clause,
    Policy,
    Control,
    SubControl,
    

    Tenant,
    Project,
    ProjectMember,
    ProjectTask,
    ProjectClause,
    TenantPolicy,
    ProjectControl,
    ProjectSubControl,
    Comment,
    Note,
    AuditorFeedback
)

# Register your models here.
admin.site.register(Framework)
admin.site.register(Task)
admin.site.register(Clause)
admin.site.register(Policy)
admin.site.register(Control)





admin.site.register(Tenant)
admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(ProjectTask)
admin.site.register(ProjectClause)
admin.site.register(TenantPolicy)
admin.site.register(ProjectControl)
admin.site.register(SubControl)
admin.site.register(ProjectSubControl)

admin.site.register(Comment)
admin.site.register(Note)
admin.site.register(AuditorFeedback)
