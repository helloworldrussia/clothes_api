from rest_framework.serializers import ModelSerializer

from telegram.models import TelegramUser, TelegramText


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'


class TelegramTextSerializer(ModelSerializer):
    class Meta:
        model = TelegramText
        fields = '__all__'
