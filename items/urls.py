from django.urls import path, include
from rest_framework.routers import SimpleRouter

from items.views import ItemViewSet, MediaFileViewSet, CategoryViewSet, BrandViewSet
from telegram.views import TelegramUserViewSet, TelegramTextViewSet

router = SimpleRouter()

router.register(r'item', ItemViewSet)
router.register(r'media_group', MediaFileViewSet, 'mediaFile')
router.register(r'category', CategoryViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'telegram-user', TelegramUserViewSet, 'telegram-user')
router.register(r'telegram-text', TelegramTextViewSet, 'telegram-text')

urlpatterns = [
    path('', include(router.urls)),
]
