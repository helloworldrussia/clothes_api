from django.contrib import admin
from telegram.models import TelegramUser, TelegramText


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    pass


@admin.register(TelegramText)
class TelegramTextAdmin(ModelAdmin):
    pass