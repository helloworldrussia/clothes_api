from django.db import models

from telegram.models import TelegramUser


class Brand(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.title}'


class MediaFile(models.Model):
    file_id = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.pk}: {self.file_id}'


class Item(models.Model):
    GENDER_CHOICES = (
        (1, 'М'),
        (2, 'Ж'),
        (3, 'Унисекс')
    )

    QUALITY_CHOICES = (
        (1, 'Top quality'),
        (2, 'High quality - AAA +'),
        (3, '1: 1🤩'))

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=555)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES)
    quality = models.PositiveSmallIntegerField(choices=QUALITY_CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    media_group = models.ManyToManyField(MediaFile, blank=True, null=True)
    category = models.ManyToManyField(Category)
    brand = models.ManyToManyField(Brand)
    subscribers = models.ManyToManyField(TelegramUser, blank=True, null=True)

    def __str__(self):
        return f'{self.pk}: {self.title}'
