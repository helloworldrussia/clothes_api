from django.test import TestCase
from django.db import IntegrityError, transaction

from telegram.models import TelegramText, TelegramUser
from telegram.serizalizers import TelegramTextSerializer, TelegramUserSerializer


class TelegramUserSerializerTestCase(TestCase):
    def test_ok(self):
        telegram_user_1 = TelegramUser.objects.create(telegram_id=313131)
        telegram_user_2 = TelegramUser.objects.create(telegram_id=323232, is_staff=True)
        telegram_user_3 = TelegramUser.objects.create(telegram_id=333333, is_staff=False)

        try:
            with transaction.atomic():
                TelegramUser.objects.create(telegram_id=313131)
            self.fail('Сериализатор допустил дубликат. Значение поля telegram_id должно быть уникальным')
        except IntegrityError:
            pass

        telegram_users = TelegramUser.objects.all()
        data = TelegramUserSerializer(telegram_users, many=True).data
        expected_data = [{"id": telegram_user_1.id, "telegram_id": 313131, "is_staff": False},
                         {"id": telegram_user_2.id, "telegram_id": 323232, "is_staff": True},
                         {"id": telegram_user_3.id, "telegram_id": 333333, "is_staff": False}]

        self.assertEqual(data, expected_data)


class TelegramTextSerializerTestCase(TestCase):
    def test_ok(self):
        text = """It is a long established fact that a reader will be distracted by the readable content
         of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal 
         distribution of letters, as opposed to using 'Content here, content here', making it look like readable 
         English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text,
          and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have 
          evolved over the years, sometimes by accident, sometimes on purpose 
          (injected humour and the like).😃⭐️➡️✅❌🔍"""
        telegram_text_1 = TelegramText.objects.create(body='', name='FAQ')
        telegram_text_2 = TelegramText.objects.create(body=text, name='Contacts')
        try:
            with transaction.atomic():
                TelegramText.objects.create(body='....', name='FAQ')
            self.fail("Значение в поле name должно быть уникальным")
        except IntegrityError:
            pass
        telegram_texts = TelegramText.objects.all()
        data = TelegramTextSerializer(telegram_texts, many=True).data
        expected_data = [{"id": telegram_text_1.id, "body": "", "name": "FAQ"},
                         {"id": telegram_text_2.id, "body": text, "name": "Contacts"}]
        self.assertEqual(data, expected_data)
