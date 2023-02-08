from django.contrib import admin
from django.contrib.admin import ModelAdmin

from items.models import Item, MediaFile, Category, Brand, TelegramUser


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    pass


@admin.register(MediaFile)
class MediaFileAdmin(ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    pass


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    pass
