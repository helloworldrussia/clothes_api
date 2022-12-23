from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from items.mixins import PageNumberSetPagination
from items.models import Item, MediaFile, Category, Brand, TelegramUser, TelegramText
from items.serializers import ItemGetSerializer, MediaFileSerializer, CategorySerializer, BrandSerializer, \
    ItemSerializer, TelegramUserSerializer, TelegramTextSerializer


class ItemViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Item.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['category', 'gender', 'price', 'quality', 'brand', 'subscribers']
    search_fields = ['title', 'description']
    pagination_class = PageNumberSetPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ItemGetSerializer
        return ItemSerializer


class MediaFileViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


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
