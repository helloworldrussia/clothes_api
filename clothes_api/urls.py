from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from items.views import ItemViewSet, CategoryViewSet, MediaFileViewSet, BrandViewSet
from telegram.views import TelegramUserViewSet, TelegramTextViewSet

router = SimpleRouter()

router.register(r'item', ItemViewSet)
router.register(r'media_group', MediaFileViewSet, 'mediaFile')
router.register(r'category', CategoryViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'telegram-user', TelegramUserViewSet, 'telegram-user')
router.register(r'telegram-text', TelegramTextViewSet, 'telegram-text')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', views.obtain_auth_token, name='token-auth')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
