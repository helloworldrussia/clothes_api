import json

from django.urls import reverse
from django.test.utils import CaptureQueriesContext
from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase

from items.mixins import PageNumberSetPagination
from items.models import Item, Brand, MediaFile, Category, TelegramUser
from items.serializers import ItemGetSerializer, MediaFileSerializer, CategorySerializer, BrandSerializer


class ItemsApiTestCase(APITestCase):
    def setUp(self):
        PageNumberSetPagination.page_size = 3

        self.telegram_user_1 = TelegramUser.objects.create(telegram_id=1786, is_staff=True)
        self.category_1 = Category.objects.create(title="Куртки")
        self.brand_1 = Brand.objects.create(title="Gucci")
        self.media_file_1 = MediaFile.objects.create(file_id="first-example-file-id")

        self.item_1 = Item.objects.create(
            title="Синяя куртка", description="Синяя куртка от производителя. Размеры: XL, L",
            gender=1, quality=1,
            price=2345
        )

        self.item_2 = Item.objects.create(
            title="Красная футболка", description="Красная футболка. Дорого. Размеры: XL, L, M",
            gender=2, quality=2, price=1390)
        self.item_2.media_group.set([self.media_file_1])
        self.item_2.category.set([self.category_1])
        self.item_2.subscribers.set([self.telegram_user_1])
        self.item_2.brand.set([self.brand_1])

        self.item_3 = Item.objects.create(
            title="Футболка-поло (зеленая)", description="Брендовое поло.",
            gender=2, quality=2, price=1390)
        self.item_3.media_group.set([self.media_file_1])
        self.item_3.category.set([self.category_1])
        self.item_3.subscribers.set([self.telegram_user_1])
        self.item_3.brand.set([self.brand_1])

    def test_get(self):
        url = reverse('item-list')
        # тест на количество запросов к бд
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(6, len(queries))
        items = Item.objects.filter(id__in=[self.item_1.id, self.item_2.id, self.item_3.id])
        serializer_data = ItemGetSerializer(items, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter(self):
        url = reverse('item-list')
        data = {
            "price": 1390.00, "category": [self.category_1.id],
            "gender": 2, "quality": 2,
            "brand": [self.brand_1.id], "subscribers": [self.telegram_user_1.id]
        }
        response = self.client.get(url, data=data)
        items = Item.objects.filter(id__in=[self.item_3.id, self.item_2.id])
        serializer_data = ItemGetSerializer(items, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        url = reverse('item-list')
        data = {
            "title": "Розовая футболка", "description": "Размеры: XL, L, M",
            "gender": 2, "quality": 2,
            "price": '1390.00', "media_group": [self.media_file_1.id],
            "brand": [self.brand_1.id], "category": [self.category_1.id],
            "subscribers": [self.telegram_user_1.id]
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        data['id'] = Item.objects.last().id
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data, response.data)

    def test_update(self):
        url = reverse('item-detail', args=(self.item_2.id,))
        data = {
            "title": "Красная футболка V2", "description": "description v2",
            "gender": 3, "quality": 3,
            "price": '7777.00', "media_group": [],
            "category": [], "brand": [],
            "subscribers": []
        }
        json_data = json.dumps(data)
        response = self.client.put(path=url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url)
        data['id'], data['gender'], data['quality'] = self.item_2.id, 'Унисекс', '1: 1🤩'
        self.assertEqual(response.data, data)

    def test_delete(self):
        url = reverse('item-detail', args=(self.item_2.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MediaFilesApiTestCase(APITestCase):
    def setUp(self):
        self.media_file_1 = MediaFile.objects.create(file_id="first-example-file-id")
        self.media_file_2 = MediaFile.objects.create(file_id="second-example-file-id")

    def test_get(self):
        url = reverse('mediaFile-list')
        # тест на количество запросов к бд
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(1, len(queries))
        media_files = MediaFile.objects.filter(id__in=[self.media_file_1.id, self.media_file_2.id])
        serializer_data = MediaFileSerializer(media_files, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        url = reverse('mediaFile-list')
        data = {"file_id": "test_file_id"}
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        data['id'] = MediaFile.objects.last().id
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data, response.data)

    def test_update(self):
        url = reverse('mediaFile-detail', args=(self.media_file_1.id,))
        data = {"file_id": "test_file_id_v2"}
        json_data = json.dumps(data)
        response = self.client.put(path=url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url)
        data['id'] = self.media_file_1.id
        self.assertEqual(response.data, data)

    def test_delete(self):
        url = reverse('mediaFile-detail', args=(self.media_file_1.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategoryApiTestCase(APITestCase):
    def setUp(self):
        self.category_1 = Category.objects.create(title="Футболки")
        self.category_2 = Category.objects.create(title="Куртки")

    def test_get(self):
        url = reverse('category-list')
        # тест на количество запросов к бд
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(3, len(queries))
        categories = Category.objects.filter(id__in=[self.category_1.id, self.category_2.id])
        serializer_data = CategorySerializer(categories, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        url = reverse('category-list')
        data = {"title": "Джинсы"}
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        data['id'] = Category.objects.last().id
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data, response.data)

    def test_update(self):
        url = reverse('category-detail', args=(self.category_1.id,))
        data = {"title": "Рубашки"}
        json_data = json.dumps(data)
        response = self.client.put(path=url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url)
        data['id'] = self.category_1.id
        self.assertEqual(response.data, data)

    def test_delete(self):
        url = reverse('category-detail', args=(self.category_1.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BrandApiTestCase(APITestCase):
    def setUp(self):
        self.brand_1 = Brand.objects.create(title="Nike")
        self.brand_2 = Brand.objects.create(title="Kappa")

    def test_get(self):
        url = reverse('brand-list')
        # тест на количество запросов к бд
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(3, len(queries))
        brands = Brand.objects.filter(id__in=[self.brand_1.id, self.brand_2.id])
        serializer_data = BrandSerializer(brands, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        url = reverse('brand-list')
        data = {"title": "Bershka"}
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        data['id'] = Brand.objects.last().id
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data, response.data)

    def test_update(self):
        url = reverse('brand-detail', args=(self.brand_1.id,))
        data = {"title": "Gucci"}
        json_data = json.dumps(data)
        response = self.client.put(path=url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url)
        data['id'] = self.brand_1.id
        self.assertEqual(response.data, data)

    def test_delete(self):
        url = reverse('brand-detail', args=(self.brand_1.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)