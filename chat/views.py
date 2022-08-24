from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from chat.filters import ChatMessageFilter
from chat.models import ChatMessage
from chat.permissions import IsChatOwner
from chat.serialisers import ChatMessageSerializer


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


class ChatMessageViewSet(ModelViewSet):
    """ Сообщения и ответы в службу поддержки. """
    serializer_class = ChatMessageSerializer
    queryset = ChatMessage.objects.select_related("user")
    http_method_names = ("get", "post")
    permission_classes = [IsAuthenticated, IsChatOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]