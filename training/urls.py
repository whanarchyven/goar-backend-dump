from rest_framework.routers import DefaultRouter

from training.views import TrainingViewSet, LectureViewSet

router = DefaultRouter()

router.register("training", TrainingViewSet, basename='training')
router.register("lecture", LectureViewSet, basename='lecture')

app_name = "api"
urlpatterns = router.urls
