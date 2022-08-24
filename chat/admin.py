from django.contrib import admin

from chat.models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_filter = ('user', )
    list_display = ('message_type', 'message', 'date', 'user')
    search_fields = ('user', 'message')
    raw_id_fields = ('user', )
