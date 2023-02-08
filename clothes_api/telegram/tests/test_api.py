import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from rest_framework.authtoken.models import Token

from telegram.models import TelegramText, TelegramUser
from telegram.serizalizers import TelegramTextSerializer, TelegramUserSerializer


class TelegramUsersApiTestCase(APITestCase):
    def setUp(self):
        self.telegram_user_1 = TelegramUser.objects.create(telegram_id=12345678, is_staff=True)
        self.telegram_user_2 = TelegramUser.objects.create(telegram_id=87654321, is_staff=False)
        self.user = User.objects.create_superuser(username='username', password='12345')
        self.headers = {"HTTP_AUTHORIZATION": f'Token {Token.objects.get(user=self.user)}'}

    def test_get(self):
        url = reverse('telegram-user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # тест на количество запросов к бд
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url, None, **self.headers)
            self.assertEqual(2, len(queries))
        telegram_users = TelegramUser.objects.filter(id__in=[self.telegram_user_1.id, self.telegram_user_2.id])
        serializer_data = TelegramUserSerializer(telegram_users, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        url = reverse('telegram-user-list')
        data = {"telegram_id": 123}
        response = self.client.post(url, data, **self.headers)
        data['id'], data['is_staff'] = TelegramUser.objects.last().id, False
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data, response.data)

    def test_update(self):
        url = reverse('telegram-user-detail', args=(self.telegram_user_2.id,))
        data = {"is_staff": True}
        response = self.client.patch(url, data, **self.headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url, None, **self.headers)
        data['id'], data['telegram_id'] = self.telegram_user_2.id, self.telegram_user_2.telegram_id
        self.assertEqual(response.data, data)

    def test_delete(self):
        url = reverse('telegram-user-detail', args=(self.telegram_user_2.id,))
        response = self.client.get(url, None, **self.headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.delete(url, None, **self.headers)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url, None, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TelegramTextsApiTestCase(APITestCase):
    def setUp(self):
        self.test_texts_body = """It is a long established fact that a reader will be distracted by the readable content
         of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal 
         distribution of letters, as opposed to using 'Content here, content here', making it look like readable 
         English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text,
          and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have 
          evolved over the years, sometimes by accident, sometimes on purpose 
          (injected humour and the like).😃⭐️➡️✅❌🔍"""
        self.telegram_text_1 = TelegramText.objects.create(body=self.test_texts_body, name="FAQ")
        self.telegram_text_2 = TelegramText.objects.create(body='Hello World', name="Contacts")

    def test_get(self):
        url = reverse('telegram-text-list')
        # тест на количество запросов к бд
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(1, len(queries))
        telegram_texts = TelegramText.objects.filter(id__in=[self.telegram_text_1.id, self.telegram_text_2.id])
        serializer_data = TelegramTextSerializer(telegram_texts, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        url = reverse('telegram-text-list')
        data = {"name": "Quick Start", "body": self.test_texts_body}
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        data['id'] = TelegramText.objects.last().id
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data, response.data)

    def test_update(self):
        url = reverse('telegram-text-detail', args=(self.telegram_text_1.id,))
        data = {"name": "About Us", "body": "Text v2"}
        json_data = json.dumps(data)
        response = self.client.put(path=url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(url)
        data['id'] = self.telegram_text_1.id
        self.assertEqual(response.data, data)

    def test_delete(self):
        url = reverse('telegram-text-detail', args=(self.telegram_text_1.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
