from django_filters import NumberFilter, ModelChoiceFilter
from django_filters.rest_framework import FilterSet, BooleanFilter

from food.models import Recipe, Favorite

filterset_fields = ['recipe_type', 'satisfying',
                    'sweet', 'simple', 'exquisite', 'speed',
                    'calories', ]

class RecipeFilter(FilterSet):
    calories = NumberFilter(field_name='calories', lookup_expr='lte')
    favorites = BooleanFilter(field_name='favorites', method='in_favorites_filter')

    class Meta:
        model = Recipe
        fields = (
            "calories",
            "recipe_type",
            "satisfying",
            "sweet",
            "simple",
            "exquisite",
            "speed",
            "favorites"
        )

    def in_favorites_filter(self, queryset, name, value):
        if value:
            favorites_ids = Favorite.objects.filter(
                user=self.request.user,
                recipe__in=queryset.all()
            ).values_list('recipe_id', flat=True)
            return queryset.filter(**{
                'id__in': favorites_ids,
            })
        return queryset

