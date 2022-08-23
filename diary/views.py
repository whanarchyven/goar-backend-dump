from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from courses.models import CourseDay
from diary.filters import DateDayFilter
from diary.serialisers import ClassDayDiarySerializer


class ClassDayDiaryViewSet(ReadOnlyModelViewSet):
    """Дневник пользователя."""
    serializer_class = ClassDayDiarySerializer
    queryset = CourseDay.objects.prefetch_related("dairy", "tasks")
    http_method_names = ("get",)
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DateDayFilter

