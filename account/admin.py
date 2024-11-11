from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import (
    Account,
    Organization
)

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = [
        "mobile",
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
        (None, {'fields': ('mobile', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()