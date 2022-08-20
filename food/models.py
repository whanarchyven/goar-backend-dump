from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

def _image_path(instance, filename):
    return '{}/{}/{}/{}/{}'.format(
        datetime.now().strftime("%Y"),
        datetime.now().strftime("%m"),
        datetime.now().strftime("%d"),
        datetime.now().strftime("%H%M"),
        filename
    )

RECIPE_TYPE = [
    ('breakfast', 'Завтрак'),
    ('lunch', 'Обед'),
    ('dinner', 'Ужин'),
    ('snack', 'Перекус'),
]

SPEED_CHOICES = [
    ('quickly', 'Быстро'),
    ('slowly', 'Без спешки'),
]

class Product(models.Model):
    """Продукты."""
    name = models.CharField("Название продукта", max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Recipe(models.Model):
    """Рецепты."""
    name = models.CharField("Название рецепта", max_length=300)
    image = models.ImageField("Изображение", upload_to=_image_path)
    recipe_type = models.CharField(
        "Тип",
        choices=RECIPE_TYPE,
        max_length=20,
        default='breakfast'
    )
    satisfying = models.BooleanField("Сытный", default=False)
    sweet = models.BooleanField("Сладкий", default=False)
    simple = models.BooleanField("Простой", default=False)
    exquisite = models.BooleanField("Изысканный", default=False)
    speed = models.CharField(
        "Скорость",
        choices=SPEED_CHOICES,
        max_length=20,
        default='quickly'
    )
    cooking_method = models.TextField("Способ приготовления")
    cooking_time = models.PositiveIntegerField("Время приготовления в минутах")
    calories = models.PositiveIntegerField("Калории")
    protein = models.PositiveIntegerField("Белок")
    fats = models.PositiveIntegerField("Жиры")
    carbohydrates = models.PositiveIntegerField("Углеводы")
    products = models.ManyToManyField(Product, through='RecipeProduct')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeProduct(models.Model):
    """Рецепт Продукт"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField("Количество")
    unit = models.CharField("Единица измерения", max_length=50)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"


class Favorite(models.Model):
    """Избранные рецепты."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return self.recipe.name

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        unique_together = ['user', 'recipe']
