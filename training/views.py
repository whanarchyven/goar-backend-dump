from django.db.models import Count, Q
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from training.models import Training
from training.serialisers import TrainingSerializer, TrainingFavoritesSerializer


class TrainingViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """ Тренировки. """
    serializer_class = TrainingSerializer
    queryset = Training.objects.prefetch_related("favorites")
    http_method_names = ("get", "post")
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.annotate(in_favorites=Count('favorites', filter=Q(favorites__user=self.request.user)))

    @action(detail=False, methods=["post"],
            permission_classes=(IsAuthenticated,),
            url_path="toggle-favorites",
            serializer_class=TrainingFavoritesSerializer)
    def toggle_favorites(self, request):
        """ Добавить или удалить из избранного. """
        serializer = self.serializer_class(
            data={
                "training_id": request.data.get("training_id"),
            },
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        favorite = serializer.save()
        if favorite:
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.data)
