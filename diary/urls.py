from rest_framework.routers import DefaultRouter

from diary.views import ClassDayDiaryViewSet

router = DefaultRouter()

router.register("dairy", ClassDayDiaryViewSet, basename='dairy')

app_name = "api"
urlpatterns = router.urls
