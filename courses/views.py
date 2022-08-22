from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from courses.models import CourseDay
from courses.serialisers import CourseDaySerializer, CourseDayTaskUserSerializer


class CourseDayViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """ Дни курса. """
    serializer_class = CourseDaySerializer
    queryset = CourseDay.objects.prefetch_related("tasks", "task_status")
    http_method_names = ("get", "post")
    permission_classes = [IsAuthenticated, ]

    @action(detail=True, methods=["post"],
            permission_classes=(IsAuthenticated,),
            url_path="toggle-task-status",
            serializer_class=CourseDayTaskUserSerializer)
    def toggle_task_status(self, request, pk=None):
        """ Обновить статус выполнения задачи. """
        serializer = self.serializer_class(
            data={
                "task_id": request.data.get("task_id"),
            },
            context={"request": request, "course_day_id": pk}
        )
        serializer.is_valid(raise_exception=True)
        done = serializer.save()
        if done:
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.data)
