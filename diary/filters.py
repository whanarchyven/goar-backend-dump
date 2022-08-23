from django_filters import DateFilter
from django_filters.rest_framework import FilterSet

from courses.models import CourseDay


class DateDayFilter(FilterSet):
    date_of_day__lte = DateFilter(field_name='date_of_day', lookup_expr='lte')
    date_of_day__gte = DateFilter(field_name='date_of_day', lookup_expr='gte')

    class Meta:
        model = CourseDay
        fields = (
            "date_of_day__lte",
            "date_of_day__gte"
        )
