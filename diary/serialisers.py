from rest_framework import serializers

from courses.models import CourseDay
from courses.serialisers import TaskSerializer
from diary.models import ClassDayDiary


class ClassDayDiarySerializer(serializers.ModelSerializer):
    """День в дневнике."""
    tasks = TaskSerializer(many=True)
    steps = serializers.SerializerMethodField()
    training = serializers.SerializerMethodField()
    water = serializers.SerializerMethodField()
    food = serializers.SerializerMethodField()
    mood = serializers.SerializerMethodField()
    increased_activity = serializers.SerializerMethodField()
    fasting_day = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    waist_circumference = serializers.SerializerMethodField()
    hip_circumference = serializers.SerializerMethodField()
    chest_volume = serializers.SerializerMethodField()

    class Meta:
        model = CourseDay
        fields = [
            'id',
            'number',
            'tasks',
            'date_of_day',
            'tip_of_the_day',
            'steps',
            'training',
            'water',
            'food',
            'mood',
            'increased_activity',
            'fasting_day',
            'weight',
            'waist_circumference',
            'hip_circumference',
            'chest_volume',
        ]

    def get_steps(self, obj) -> bool:
        """Пройдены ли шаги"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.steps
        except ClassDayDiary.DoesNotExist:
            return False

    def get_training(self, obj) -> bool:
        """Пройдена ли тренировка"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.training
        except ClassDayDiary.DoesNotExist:
            return False

    def get_water(self, obj) -> bool | int:
        """Количество выпитой воды в мл"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.water
        except ClassDayDiary.DoesNotExist:
            return False

    def get_food(self, obj) -> bool:
        """Питание"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.food
        except ClassDayDiary.DoesNotExist:
            return False

    def get_mood(self, obj) -> str | bool:
        """Настроение"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.mood
        except ClassDayDiary.DoesNotExist:
            return False

    def get_increased_activity(self, obj) -> bool:
        """Повышенная активность на протяжении дня"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.increased_activity
        except ClassDayDiary.DoesNotExist:
            return False

    def get_fasting_day(self, obj) -> bool:
        """Разгрузочный день"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.fasting_day
        except ClassDayDiary.DoesNotExist:
            return False

    def get_weight(self, obj) -> bool | int:
        """Вес"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.weight
        except ClassDayDiary.DoesNotExist:
            return False

    def get_waist_circumference(self, obj) -> bool | int:
        """ОТ"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.waist_circumference
        except ClassDayDiary.DoesNotExist:
            return False

    def get_hip_circumference(self, obj) -> bool | int:
        """ОБ"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.hip_circumference
        except ClassDayDiary.DoesNotExist:
            return False

    def get_chest_volume(self, obj) -> bool | int:
        """ОТ"""
        try:
            dairy_day = obj.dairy.get(
                user=self.context['request'].user,
            )
            return dairy_day.chest_volume
        except ClassDayDiary.DoesNotExist:
            return False


class ClassDayDiaryUpdateSerializer(serializers.ModelSerializer):
    """Обновление данных в дневнике"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ClassDayDiary
        fields = [
            'id',
            'user',
            'mood',
            'increased_activity',
            'fasting_day',
            'steps',
            'training',
            'water',
            'food',
            'weight',
            'waist_circumference',
            'hip_circumference',
            'chest_volume'
        ]
