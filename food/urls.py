from rest_framework.routers import DefaultRouter

from food.views import RecipeViewSet

router = DefaultRouter()

router.register("recipes", RecipeViewSet, basename='recipes')

app_name = "api"
urlpatterns = router.urls
