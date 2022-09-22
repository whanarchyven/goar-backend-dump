import threading

from django.contrib.auth import get_user_model, user_logged_in
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenViewBase

from users import login_user
from users.models import Profile
from users.permissions import IsProfileOwner
from users.serialisers import UserSerializer, ProfileSerializer, RegistrationSerializer, ProfileImageSerializer, \
    ProfilePhotoBeforeSerializer, ProfilePhotoAfterSerializer
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
        "Поздравляю, вы получили доступ к моей программе «Метод Гоар»",
        'email.txt',
        email,
        {"email": email, "password": password},
        'email.html'
    )

class UserExists(APIException):
    status_code = 400
    default_detail = 'Пользователь с таким email уже зарегистрирован'


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """ Профиль. Выдает массив, в котором только один профиль
    текущего пользователя
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related("user")
    http_method_names = ("get", "patch", "post")
    permission_classes = [IsAuthenticated, IsProfileOwner]
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["post"],
            url_path="update-profile-image",
            permission_classes=(IsAuthenticated, ),
            serializer_class=ProfileImageSerializer)
    def update_profile_image(self, request):
        """Обновляет фото профиля. """
        profile = request.user.profile
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


    @action(detail=False, methods=["post"],
            url_path="update-photo-before",
            permission_classes=(IsAuthenticated, ),
            serializer_class=ProfilePhotoBeforeSerializer)
    def update_photo_before(self, request):
        """Обновляет фото до. """
        profile = request.user.profile
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


    @action(detail=False, methods=["post"],
            url_path="update-photo-after",
            permission_classes=(IsAuthenticated, ),
            serializer_class=ProfilePhotoAfterSerializer)
    def update_photo_after(self, request):
        """Обновляет фото до. """
        profile = request.user.profile
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


    @action(detail=False,
            methods=["POST"],
            http_method_names=("post",),
            url_name="register", permission_classes=(AllowAny,),
            serializer_class=RegistrationSerializer)
    def register(self, request):
        """Регистрация нового пользователя."""
        if 'email' not in request.data:
            return Response(status=status.HTTP_200_OK)
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        try:
            User.objects.get(
                email=request.data['email']
            )
            raise UserExists
        except User.DoesNotExist:
            password = User.objects.make_random_password()
            thread = threading.Thread(target=send_email, args=(
                request.data['email'],
                password
            ))
            thread.start()
            # send_email(request.data['email'], password)

            serializer.save(password=password)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER

    def post(self, request, *args, **kwargs):
        login_user.send(sender=User, request=request, user=request.user)
        return super().post(request, *args, **kwargs)
