from rest_framework.test import APITestCase

from items.filters import ItemDetailsFilterSet
from items.mixins import PageNumberSetPagination
from items.models import Item, Brand, Category, MediaFile
from telegram.models import TelegramUser


class ItemDetailsFilterSetTestCase(APITestCase):
    def setUp(self):
        self.telegram_user_1 = TelegramUser.objects.create(telegram_id=1786, is_staff=True)
        self.media_file_1 = MediaFile.objects.create(file_id="first-example-file-id")
        self.media_file_2 = MediaFile.objects.create(file_id="second-example-file-id")

        self.category_1 = Category.objects.create(title="Куртки")
        self.category_2 = Category.objects.create(title="Футболки")
        self.category_3 = Category.objects.create(title="Штаны")

        self.brand_1 = Brand.objects.create(title="Gucci")
        self.brand_2 = Brand.objects.create(title="Nike")
        self.brand_3 = Brand.objects.create(title="Puma")

        self.item_1 = Item.objects.create(
            title="Синяя куртка", description="Синяя куртка от производителя. Размеры: XL, L",
            gender=1, quality=1,
            price=2345
        )
        self.item_1.category.set([self.category_1])
        self.item_1.brand.set([self.brand_1])

        self.item_2 = Item.objects.create(
            title="Красная футболка", description="Красная футболка. Дорого. Размеры: XL, L, M",
            gender=2, quality=2, price=1390)
        self.item_2.category.set([self.category_2])
        self.item_2.brand.set([self.brand_2])
        self.item_2.media_group.set([self.media_file_1])

        self.item_3 = Item.objects.create(
            title="Футболка-поло (зеленая)", description="Брендовое поло.",
            gender=2, quality=2, price=1390)
        self.item_3.category.set([self.category_1])
        self.item_3.brand.set([self.brand_3])
        self.item_3.subscribers.set([self.telegram_user_1])

    def test_ok(self):
        filter_params = {
            'gender': [2],
        }
        queryset = Category.objects.all()
        filtered = ItemDetailsFilterSet(
            filter_params, queryset
        )
        expected_data = [
            self.category_2,
            self.category_1,
        ]
        self.assertEqual(list(filtered.qs), expected_data)

        queryset = Brand.objects.all()
        filtered = ItemDetailsFilterSet(
            filter_params, queryset
        )
        expected_data = [
            self.brand_2,
            self.brand_3,
        ]
        self.assertEqual(list(filtered.qs), expected_data)

    def test_complex_filtration(self):
        filter_params = {
            'gender': [2],
            'quality': [2],
            'brand': [self.brand_3],
        }

        queryset = Category.objects.all()
        filtered = ItemDetailsFilterSet(
            filter_params, queryset
        )

        self.assertEqual(list(filtered.qs), [self.category_1])

        del filter_params['brand']
        filter_params['category'] = [self.category_1]

        queryset = Brand.objects.all()
        filtered = ItemDetailsFilterSet(
            filter_params, queryset
        )

        self.assertEqual(list(filtered.qs), [self.brand_3])
