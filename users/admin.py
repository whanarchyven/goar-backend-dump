from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import FitnessUser, UserLoginActivity

admin.site.site_header = "Метод Гоар"
admin.site.site_title = "Метод Гоар"
admin.site.index_title = "Метод Гоар"


@admin.register(FitnessUser)
class FitnessUserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_admin", "number_of_devices")
    list_filter = ("is_admin", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)

    def number_of_devices(self, obj):
        try:
            number_of_devices = UserLoginActivity.objects.filter(
                login_email=obj.email
            ).distinct("user_agent_info").count()
        except:
            number_of_devices = 0
        return number_of_devices

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
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
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


# admin.site.unregister(User)
admin.site.register(User, FitnessUserAdmin)

@admin.register(UserLoginActivity)
class UserLoginActivityAdmin(admin.ModelAdmin):
    list_display = ("login_email", "login_IP", "user_agent_info", "login_datetime")
    list_filter = ("login_email", )