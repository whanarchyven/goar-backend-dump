from django.contrib import admin

from courses.models import CourseDay, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 5


@admin.register(CourseDay)
class CourseDayAdmin(admin.ModelAdmin):
    inlines = [TaskInline, ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
