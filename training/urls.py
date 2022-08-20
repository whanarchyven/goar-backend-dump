from rest_framework.routers import DefaultRouter

from training.views import TrainingViewSet

router = DefaultRouter()

router.register("training", TrainingViewSet, basename='training')

app_name = "api"
urlpatterns = router.urls
