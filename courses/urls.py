from rest_framework.routers import DefaultRouter

from courses.views import CourseDayViewSet

router = DefaultRouter()

router.register("course", CourseDayViewSet, basename='course')

app_name = "api"
urlpatterns = router.urls
