from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import (
    Account
)

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = [
        "email",
        "username",
        "role",
        "is_superuser",
        "is_admin",
        "is_staff"
    ]
    search_fields = (
        "pk",
        "email",
        "username",
    )
    readonly_fields = ("pk", "date_joined", "last_login")



    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
