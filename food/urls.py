from rest_framework.routers import DefaultRouter

from food.views import RecipeViewSet, FoodIntakeViewSet, CustomFoodIntakeViewSet

router = DefaultRouter()

router.register("recipes", RecipeViewSet, basename='recipes')
router.register("food-intake", FoodIntakeViewSet, basename='food-intake')
router.register("custom-food-intake", CustomFoodIntakeViewSet, basename='custom-food-intake')

app_name = "api"
urlpatterns = router.urls
