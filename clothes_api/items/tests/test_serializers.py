from django.db import IntegrityError
from django.test import TestCase

from items.models import MediaFile, Brand, Category, TelegramUser, Item
from items.serializers import MediaFileSerializer, BrandSerializer, CategorySerializer,\
    ItemSerializer, ItemGetSerializer
from django.db import transaction


class ItemGetSerializerTestCase(TestCase):
    def test_ok(self):
        telegram_user_1 = TelegramUser.objects.create(telegram_id=1784)
        telegram_user_2 = TelegramUser.objects.create(telegram_id=1786, is_staff=True)
        category_1 = Category.objects.create(title="Куртки")
        category_2 = Category.objects.create(title="Футболки")
        brand_1 = Brand.objects.create(title="Gucci")
        brand_2 = Brand.objects.create(title="Bershka")
        media_file_1 = MediaFile.objects.create(file_id="first-example-file-id")
        media_file_2 = MediaFile.objects.create(file_id="second-example-file-id")
        item_1 = Item.objects.create(
            title="Синяя куртка", description="Синяя куртка от производителя. Размеры: XL, L",
            gender=1, quality=1,
            price=2345
        )
        item_2 = Item.objects.create(
            title="Красная футболка", description="Красная футболка. Дорого. Размеры: XL, L, M",
            gender=2, quality=2, price=1390)
        item_2.media_group.set([media_file_1])
        item_2.category.set([category_1])
        item_2.subscribers.set([telegram_user_1])
        item_2.brand.set([brand_1])
        item_3 = Item.objects.create(
            title="Зеленая куртка (футболка в подарок)", description="Брендовая куртка с подарком.",
            gender=3, quality=3, price=5230)
        item_3.media_group.set([media_file_1, media_file_2])
        item_3.category.set([category_1, category_2])
        item_3.subscribers.set([telegram_user_1, telegram_user_2])
        item_3.brand.set([brand_1, brand_2])

        items = Item.objects.all()
        data = ItemGetSerializer(items, many=True).data
        expected_data = [
            {
                "id": item_1.id, "title": "Синяя куртка",
                "description": "Синяя куртка от производителя. Размеры: XL, L", "gender": "Муж",
                "quality": "Top quality", "price": "2345.00",
                "media_group": [], "category": [],
                "brand": [], "subscribers": []
            },
            {
                "id": item_2.id, "title": "Красная футболка",
                "description": "Красная футболка. Дорого. Размеры: XL, L, M", "gender": "Жен",
                "quality": "High quality - AAA +", "price": "1390.00",
                "media_group": [{"id": media_file_1.id, "file_id": "first-example-file-id"}],
                "category": [{"id": category_1.id, "title": "Куртки"}],
                "brand": [{"id": brand_1.id, "title": "Gucci"}],
                "subscribers": [telegram_user_1.id]
            },
            {
                "id": item_3.id, "title": "Зеленая куртка (футболка в подарок)",
                "description": "Брендовая куртка с подарком.", "gender": "Унисекс",
                "quality": "1:1🤩", "price": "5230.00",
                "media_group": [{"id": media_file_1.id, "file_id": "first-example-file-id"},
                                {"id": media_file_2.id, "file_id": "second-example-file-id"}],
                "category": [{"id": category_1.id, "title": "Куртки"},
                             {"id": category_2.id, "title": "Футболки"}],
                "brand": [{"id": brand_1.id, "title": "Gucci"},
                          {"id": brand_2.id, "title": "Bershka"}],
                "subscribers": [telegram_user_1.id, telegram_user_2.id]
            }
        ]

        self.assertEqual(data, expected_data)


class ItemSerializerTestCase(TestCase):
    def test_ok(self):
        telegram_user_1 = TelegramUser.objects.create(telegram_id=1784)
        telegram_user_2 = TelegramUser.objects.create(telegram_id=1786, is_staff=True)
        category_1 = Category.objects.create(title="Куртки")
        category_2 = Category.objects.create(title="Футболки")
        brand_1 = Brand.objects.create(title="Gucci")
        brand_2 = Brand.objects.create(title="Bershka")
        media_file_1 = MediaFile.objects.create(file_id="first-example-file-id")
        media_file_2 = MediaFile.objects.create(file_id="second-example-file-id")
        item_1 = Item.objects.create(
            title="Синяя куртка", description="Синяя куртка от производителя. Размеры: XL, L",
            gender=1, quality=1,
            price=2345
        )
        item_2 = Item.objects.create(
            title="Красная футболка", description="Красная футболка. Дорого. Размеры: XL, L, M",
            gender=2, quality=2, price=1390)
        item_2.media_group.set([media_file_1])
        item_2.category.set([category_1])
        item_2.subscribers.set([telegram_user_1])
        item_2.brand.set([brand_1])
        item_3 = Item.objects.create(
            title="Зеленая куртка (футболка в подарок)", description="Брендовая куртка с подарком.",
            gender=3, quality=3, price=5230)
        item_3.media_group.set([media_file_1, media_file_2])
        item_3.category.set([category_1, category_2])
        item_3.subscribers.set([telegram_user_1, telegram_user_2])
        item_3.brand.set([brand_1, brand_2])

        items = Item.objects.all()
        data = ItemSerializer(items, many=True).data
        expected_data = [
            {
                "id": item_1.id, "title": "Синяя куртка",
                "description": "Синяя куртка от производителя. Размеры: XL, L", "gender": 1,
                "quality": 1, "price": "2345.00",
                "media_group": [], "category": [],
                "brand": [], "subscribers": []
            },
            {
                "id": item_2.id, "title": "Красная футболка",
                "description": "Красная футболка. Дорого. Размеры: XL, L, M", "gender": 2,
                "quality": 2, "price": "1390.00",
                "media_group": [media_file_1.id], "category": [category_1.id],
                "brand": [brand_1.id], "subscribers": [telegram_user_1.id],
            },
            {
                "id": item_3.id, "title": "Зеленая куртка (футболка в подарок)",
                "description": "Брендовая куртка с подарком.", "gender": 3,
                "quality": 3, "price": "5230.00",
                "media_group": [media_file_1.id, media_file_2.id], "category": [category_1.id, category_2.id],
                "brand": [brand_1.id, brand_2.id], "subscribers": [telegram_user_1.id, telegram_user_2.id]
            }
        ]
        self.assertEqual(data, expected_data)


class MediaFileSerializerTestCase(TestCase):
    def test_ok(self):
        media_file_1 = MediaFile.objects.create(file_id="first-example-file-id")
        media_file_2 = MediaFile.objects.create(file_id="second-example-file-id")
        media_files = MediaFile.objects.all()
        data = MediaFileSerializer(media_files, many=True).data

        expected_data = [{"id": media_file_1.id, "file_id": "first-example-file-id"},
                         {"id": media_file_2.id, "file_id": "second-example-file-id"}]

        self.assertEqual(expected_data, data)


class BrandSerializerTestCase(TestCase):
    def test_ok(self):
        brand_1 = Brand.objects.create(title="Gucci")
        brand_2 = Brand.objects.create(title="Bershka")
        try:
            with transaction.atomic():
                Brand.objects.create(title="Gucci")
            self.fail('Сериализатор допустил дубликат. Значение поля title должно быть уникальным')
        except IntegrityError:
            pass
        brands = Brand.objects.all()
        data = BrandSerializer(brands, many=True).data

        expected_data = [{"id": brand_1.id, "title": "Gucci"},
                         {"id": brand_2.id, "title": "Bershka"}]

        self.assertEqual(expected_data, data)


class CategorySerializerTestCase(TestCase):
    def test_ok(self):
        category_1 = Category.objects.create(title="Куртки")
        category_2 = Category.objects.create(title="Футболки")
        try:
            with transaction.atomic():
                Category.objects.create(title="Футболки")
            self.fail('Сериализатор допустил дубликат. Значение поля title должно быть уникальным')
        except IntegrityError:
            pass
        category = Category.objects.all()
        data = CategorySerializer(category, many=True).data
        expected_data = [{"id": category_1.id, "title": "Куртки"},
                         {"id": category_2.id, "title": "Футболки"}]

        self.assertEqual(expected_data, data)