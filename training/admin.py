from django.contrib import admin

from training.models import Training


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    pass
