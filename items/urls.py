from rest_framework.routers import SimpleRouter

from items.views import ItemViewSet, MediaFileViewSet, CategoryViewSet, BrandViewSet, TelegramUserViewSet, \
    TelegramTextViewSet

router = SimpleRouter()

router.register(r'item', ItemViewSet)
router.register(r'media_group', MediaFileViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'telegram-user', TelegramUserViewSet)
router.register(r'telegram-text', TelegramTextViewSet)


urlpatterns = router.urls
