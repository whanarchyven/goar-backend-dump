from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from food.filters import RecipeFilter, FoodIntakeFilter
from food.models import Recipe, FoodIntake
from food.permissions import IsFoodIntake
from food.serialisers import RecipeSerializer, ToggleFavoriteSerializer, FoodIntakeAddSerializer, \
    FoodIntakeListSerializer


class RecipeViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """Рецепты
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.prefetch_related("favorites")
    http_method_names = ("get", "post")
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RecipeFilter

    def get_queryset(self):
        return self.queryset.annotate(in_favorites=Count('favorites', filter=Q(favorites__user=self.request.user)))

    @action(detail=False, methods=["post"],
            permission_classes=(IsAuthenticated,),
            url_path="toggle-favorites",
            serializer_class=ToggleFavoriteSerializer)
    def toggle_favorites(self, request):
        """ Добавить или удалить из избранного. """
        serializer = self.serializer_class(
            data={
                "recipe_id": request.data.get("recipe_id"),
            },
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        favorite = serializer.save()
        if favorite:
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.data)


class FoodIntakeViewSet(ModelViewSet):
    """Добавить, удалить, обновить, прием пищи, привязано к дню курса, можно добавить либо
       рецепт, либо вручную ввести калорийность, количество белков жиров и углеводов.
       Рецепт имеет приоритет."""
    serializer_class = FoodIntakeAddSerializer
    queryset = FoodIntake.objects.select_related("recipe")
    http_method_names = ("get", "post", "patch", "delete")
    permission_classes = [IsAuthenticated, IsFoodIntake]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FoodIntakeFilter

    def list(self, request, *args, **kwargs):
        self.serializer_class = FoodIntakeListSerializer
        return super().list(request, args, kwargs)
