from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import FitnessUser

admin.site.site_header = "Метод Гоар"
admin.site.site_title = "Метод Гоар"
admin.site.index_title = "Метод Гоар"


@admin.register(FitnessUser)
class FitnessUserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_admin")
    list_filter = ("is_admin", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("password", )}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("password1", "password2"),
            },
        ),
    )
