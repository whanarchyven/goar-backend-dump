from django.contrib import admin

from training.models import Training, Lecture


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    pass

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    pass
