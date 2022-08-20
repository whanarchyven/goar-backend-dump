from rest_framework import serializers

from training.models import Training, TrainingFavorite


class TrainingSerializer(serializers.ModelSerializer):
    """Тренировки."""
    in_favorites = serializers.SerializerMethodField()

    class Meta:
        model = Training
        fields = ['id', 'name', 'video', 'calories_rating', 'training_time', 'in_favorites']

    def get_in_favorites(self, obj):
        return obj.in_favorites > 0


class TrainingFavoritesSerializer(serializers.Serializer):
    """Тренировки."""
    training_id = serializers.IntegerField()

    def save(self, **kwargs):
        training_id = self.validated_data['training_id']
        training = Training.objects.get(id=training_id)
        user = self.context["request"].user
        created = False
        try:
            favorite = TrainingFavorite.objects.get(
                training=training,
                user=user
            )
            favorite.delete()
        except TrainingFavorite.DoesNotExist:
            TrainingFavorite.objects.create(
                training=training,
                user=user
            )
            created = True
        return created
