from rest_framework.routers import DefaultRouter

from food.views import RecipeViewSet, FoodIntakeViewSet

router = DefaultRouter()

router.register("recipes", RecipeViewSet, basename='recipes')
router.register("food-intake", FoodIntakeViewSet, basename='food-intake')

app_name = "api"
urlpatterns = router.urls
