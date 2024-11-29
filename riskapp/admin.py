from django.contrib import admin

from riskapp.models import (
    RiskMapping,
    ThreatMapping,
    RiskCategory,
    RiskScroingMethod,
    ControlRegister,
    Team,

    RiskRegister,
    MitigationControl,
    RiskMitigation,
    Review,
    PlanProject,
    ReviewProject,
    Comment
)

admin.site.register(RiskMapping)
admin.site.register(ThreatMapping)
admin.site.register(RiskCategory)
admin.site.register(RiskScroingMethod)
admin.site.register(ControlRegister)
admin.site.register(Team)

admin.site.register(RiskRegister)
admin.site.register(MitigationControl)
admin.site.register(RiskMitigation)
admin.site.register(Review)
admin.site.register(PlanProject)
admin.site.register(ReviewProject)
admin.site.register(Comment)