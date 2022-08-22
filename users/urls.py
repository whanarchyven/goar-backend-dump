from rest_framework.routers import DefaultRouter

from users.views import ProfileViewSet

router = DefaultRouter()

router.register("profile", ProfileViewSet, basename='profile')

app_name = "api"
urlpatterns = router.urls
