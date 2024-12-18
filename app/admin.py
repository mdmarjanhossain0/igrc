from django.contrib import admin
from app.models import(
    Framework,
    Task,
    Clause,
    SubClause,
    Policy,
    Control,
    SubControl,
    

    Tenant,
    Project,
    ProjectMember,
    ProjectTask,
    ProjectClause,
    ProjectSubClause,
    TenantPolicy,
    ProjectControl,
    ProjectSubControl,
    Comment,
    Note,
    AuditorFeedback,
    Evidence,
    EvidenceFile
)




admin.site.register(Framework)
admin.site.register(Task)

class SubClauseAdmin(admin.TabularInline):
    model = SubClause

class ClauseAdmin(admin.ModelAdmin):
    inlines = [SubClauseAdmin]
admin.site.register(Clause, ClauseAdmin)
admin.site.register(Policy)

class SubControlAdmin(admin.TabularInline):
    model = SubControl

class ControlAdmin(admin.ModelAdmin):
    inlines = [SubControlAdmin]
admin.site.register(Control, ControlAdmin)





admin.site.register(Tenant)
admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(ProjectTask)


class ProjectSubClauseAdmin(admin.TabularInline):
    model = ProjectSubClause

class ProjectClauseAdmin(admin.ModelAdmin):
    inlines = [ProjectSubClauseAdmin]
admin.site.register(ProjectClause, ProjectClauseAdmin)

admin.site.register(TenantPolicy)
admin.site.register(ProjectControl)
admin.site.register(ProjectSubControl)

admin.site.register(Comment)
admin.site.register(Note)
admin.site.register(AuditorFeedback)
admin.site.register(Evidence)
admin.site.register(EvidenceFile)