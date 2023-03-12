from django.contrib import admin
from telegram.models import TelegramUser, TelegramText


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass


@admin.register(TelegramText)
class TelegramTextAdmin(admin.ModelAdmin):
    pass