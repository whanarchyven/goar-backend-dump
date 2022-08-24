from rest_framework import serializers

from chat.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """Создать сообщение."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ChatMessage
        fields = ['id', 'message', 'user', 'message_type', 'date']


