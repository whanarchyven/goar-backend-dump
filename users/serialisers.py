from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import Profile
User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    """Профиль пользователя."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()


    class Meta:
        model = Profile
        fields = [
            'id',
            'weight',
            'waist_circumference',
            'hip_circumference',
            'chest_volume',
            'target_weight',
            'target_waist_circumference',
            'target_hip_circumference',
            'target_chest_volume',
            'profile_image',
            'photo_before',
            'photo_after',
            'daily_calorie_intake',
            'daily_water_intake',
            'daily_step_rate',
            'first_name',
            'last_name',
            'user'
        ]

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name



class UserSerializer(serializers.ModelSerializer):
    """Пользователь."""

    class Meta:
        model = get_user_model()
        fields = ['id', ]


class ProfileImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Profile
        fields = [
            'profile_image',
            'user'
        ]


class RegistrationSerializer(serializers.Serializer):
    """Регистрация участника."""
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    phone = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate_code(self, val):
        if val != "method_goar":
            raise ValidationError("Неправильный код")

    def save(self, **kwargs):
        user = User(
            first_name=self.validated_data['first_name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            is_active=True,
            is_admin=False,
        )
        user.set_password(kwargs['password'])
        user.save()
        return user

