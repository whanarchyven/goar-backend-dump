from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from rest_framework import serializers

from food.models import Recipe, RecipeProduct, Product, Favorite, FoodIntake


class ThumbnailSerializer(serializers.ImageField):
    def __init__(self, alias, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.read_only = True
        self.alias = alias

    def to_representation(self, value):
        if not value:
            return None

        url = thumbnail_url(value, self.alias)
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class ProductSerializer(serializers.ModelSerializer):
    """Продукт."""

    class Meta:
        model = Product
        fields = ['id', 'name']


class IngredientsSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = RecipeProduct
        fields = ['product', 'quantity', 'unit']

    def get_product(self, obj):
        return obj.product.name


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True)
    preview_image = ThumbnailSerializer(alias='small', source='image')
    in_favorites = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'recipe_type', 'satisfying', 'image',
                  'sweet', 'simple', 'exquisite', 'speed',
                  'cooking_method', 'calories', 'protein',
                  'fats', 'carbohydrates', 'cooking_time',
                  'preview_image', 'ingredients', 'in_favorites']

    def get_in_favorites(self, obj):
        return obj.in_favorites > 0


class ToggleFavoriteSerializer(serializers.Serializer):
    """Добавить или удалить из избранного"""
    recipe_id = serializers.IntegerField()

    def save(self, **kwargs):
        recipe_id = self.validated_data['recipe_id']
        recipe = Recipe.objects.get(id=recipe_id)
        user = self.context["request"].user
        created = False
        try:
            favorite = Favorite.objects.get(
                recipe=recipe,
                user=user
            )
            favorite.delete()
        except Favorite.DoesNotExist:
            Favorite.objects.create(
                recipe=recipe,
                user=user
            )
            created = True
        return created


class FoodIntakeAddSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FoodIntake
        fields = '__all__'


class RecipeFoodIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'recipe_type', 'calories', 'protein',
                  'fats', 'carbohydrates']

class FoodIntakeListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    recipe = RecipeFoodIntakeSerializer(read_only=True)

    class Meta:
        model = FoodIntake
        fields = '__all__'
