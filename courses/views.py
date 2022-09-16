from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from courses.models import CourseDay
from courses.serialisers import CourseDaySerializer, CourseDayTaskUserSerializer
from diary.models import ClassDayDiary
from diary.serialisers import ClassDayDiaryUpdateSerializer


class CourseDayViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """ Дни курса. """
    serializer_class = CourseDaySerializer
    queryset = CourseDay.objects.prefetch_related("tasks", "task_status").order_by("number", "id")
    http_method_names = ("get", "post")
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'number'

    @action(detail=True, methods=["post"],
            permission_classes=(IsAuthenticated,),
            url_path="toggle-task-status",
            serializer_class=CourseDayTaskUserSerializer)
    def toggle_task_status(self, request, number=None):
        """ Обновить статус выполнения задачи. """
        serializer = self.serializer_class(
            data={
                "task_id": request.data.get("task_id"),
            },
            context={"request": request, "course_day__number": number}
        )
        serializer.is_valid(raise_exception=True)
        done = serializer.save()
        if done:
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.data)

    @action(detail=True, methods=["post"],
            permission_classes=(IsAuthenticated,),
            url_path="update-user-dairy-day",
            serializer_class=ClassDayDiaryUpdateSerializer)
    def update_user_dairy_day(self, request, number=None):
        """ Обновить дневник пользователя на этот день курса. """
        instance, created = ClassDayDiary.objects.get_or_create(
            user=request.user,
            course_day=CourseDay.objects.get(number=number)
        )
        serializer = self.serializer_class(
            instance=instance,
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
