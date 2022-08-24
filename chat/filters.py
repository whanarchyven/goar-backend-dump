from django_filters import NumberFilter, ModelChoiceFilter
from django_filters.rest_framework import FilterSet, BooleanFilter

from chat.models import ChatMessage
from food.models import Recipe, Favorite, FoodIntake




class ChatMessageFilter(FilterSet):

    class Meta:
        model = ChatMessage
        fields = {
            "user__id": ['exact'],
        }