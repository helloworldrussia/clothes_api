from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from telegram.models import TelegramText, TelegramUser
from telegram.serizalizers import TelegramTextSerializer, TelegramUserSerializer


class TelegramUserViewSet(ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['telegram_id', 'is_staff']


class TelegramTextViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TelegramText.objects.all()
    serializer_class = TelegramTextSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']
