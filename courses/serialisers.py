from rest_framework import serializers

from courses.models import CourseDay, Task, CourseDayTaskUser


class TaskSerializer(serializers.ModelSerializer):
    """Задача на день."""
    done = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'done']

    def get_done(self, obj):
        return obj.task_status.filter(
            user=self.context['request'].user,
            course_day=obj.course_day
        ).count() > 0


class CourseDaySerializer(serializers.ModelSerializer):
    """День курса."""
    tasks = TaskSerializer(many=True)

    class Meta:
        model = CourseDay
        fields = ['id', 'number', 'date_of_day', 'tasks', 'tip_of_the_day']


class CourseDayTaskUserSerializer(serializers.Serializer):
    """Статус выполнения."""
    task_id = serializers.IntegerField()

    def save(self, **kwargs):
        user = self.context['request'].user
        course_day_id = self.context['course_day_id']
        task_id = self.validated_data['task_id']
        course_day = CourseDay.objects.get(id=course_day_id)
        task = Task.objects.get(id=task_id)
        done = False
        try:
            CourseDayTaskUser.objects.get(
                course_day=course_day,
                task=task,
                user=user
            ).delete()
        except CourseDayTaskUser.DoesNotExist:
            CourseDayTaskUser.objects.create(
                course_day=course_day,
                task=task,
                user=user
            )
            done = True
        return done
