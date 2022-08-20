from rest_framework.routers import DefaultRouter

from cart.views import CartViewSet, CartProductViewSet

router = DefaultRouter()

router.register("cart", CartViewSet, basename='cart')

app_name = "api"
urlpatterns = router.urls
