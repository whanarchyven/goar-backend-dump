import threading

from django.contrib.auth import get_user_model
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from users.models import Profile
from users.permissions import IsProfileOwner
from users.serialisers import UserSerializer, ProfileSerializer, RegistrationSerializer
from users.utils import send_new_user_email

User = get_user_model()


class UserViewSet(ModelViewSet):
    """ Пользователь. """
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related("profile")
    http_method_names = ("get", "post")
    permission_classes = [IsAuthenticated, ]


def send_email(email, password):
    send_new_user_email(
        "Доступ к платформе курса успешно оплачен",
        'email.txt',
        email,
        {"email": email, "password": password},
        'email.html'
    )


class UserExists(Exception):
    def __init__(self):
        self.message = "Пользователь с таким email уже зарегистрирован"

    def __str__(self):
        return self.message


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

    @action(detail=False,
            methods=["POST"],
            http_method_names=("post",),
            url_name="register", permission_classes=(AllowAny,),
            serializer_class=RegistrationSerializer)
    def register(self, request):
        """Регистрация нового пользователя."""
        serializer = self.serializer_class(data=request.data, context={"request": request})
        try:
            User.objects.get(
                email=request.data['email']
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=UserExists)
        except User.DoesNotExist:
            serializer.is_valid(raise_exception=True)
            password = User.objects.make_random_password()
            thread = threading.Thread(target=send_email, args=(
                request.data['email'],
                password
            ))
            thread.start()
            # send_email(request.data['email'], password)

            serializer.save(password=password)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
