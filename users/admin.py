from django.contrib import admin

from .models import FitnessUser

admin.site.site_header = "Метод Гоар"
admin.site.site_title = "Метод Гоар"
admin.site.index_title = "Метод Гоар"


@admin.register(FitnessUser)
class FitnessUserAdmin(admin.ModelAdmin):
    list_filter = ('is_admin',)
