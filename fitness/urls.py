"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from chat.views import ChatMessageViewSet
from food.urls import router as food_router
from cart.urls import router as cart_router
from training.urls import router as training_router
from courses.urls import router as courses_router
from users.urls import router as users_router
from diary.urls import router as dairy_router
from users.views import CustomTokenObtainPairView

router = DefaultRouter()
router.registry.extend(food_router.registry)
router.registry.extend(cart_router.registry)
router.registry.extend(training_router.registry)
router.registry.extend(courses_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(dairy_router.registry)
router.register("chat-message", ChatMessageViewSet, basename='chat-message')

auth_urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(auth_urlpatterns)),
    path('ws/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# swagger

schema_view = get_schema_view(
   openapi.Info(
      title="Метод Гоар API",
      default_version='v1',
      description="Документация",
      contact=openapi.Contact(email="vladislah@gmail.com"),
   ),
   public=True,
)

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('', admin.site.urls),
]
