from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from users.models import Profile
from users.permissions import IsProfileOwner
from users.serialisers import UserSerializer, ProfileSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    """ Пользователь. """
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related("profile")
    http_method_names = ("get", "post")
    permission_classes = [IsAuthenticated, ]


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """ Профиль. Выдает массив, в котором только один профиль
    текущего пользователя
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related("user")
    http_method_names = ("get", "patch")
    permission_classes = [IsAuthenticated, IsProfileOwner]
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
