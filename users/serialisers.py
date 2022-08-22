from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Profile


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


