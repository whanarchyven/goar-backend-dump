from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

MESSAGE_TYPE = [
    ('question', 'Вопрос'),
    ('answer', 'Ответ'),
]

class ChatMessage(models.Model):
    """Chat Message."""
    user = models.ForeignKey(User, related_name='user', on_delete=models.PROTECT)
    message = models.TextField('Message')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE, default='answer')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


@receiver(post_save, sender=ChatMessage)
def send_message(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{instance.user.id}',
        {
            'type': 'chat_message',
            'message': instance.message,
            'message_type': instance.message_type,
            'date': instance.date.strftime("%m/%d/%Y, %H:%M:%S")
        }
    )
