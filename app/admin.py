from django.contrib import admin
from app.models import(
    Framework,
    Task,
    Clause,
    Policy,
    Control
)

# Register your models here.
admin.site.register(Framework)
admin.site.register(Task)
admin.site.register(Clause)
admin.site.register(Policy)
admin.site.register(Control)
