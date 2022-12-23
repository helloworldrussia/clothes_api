from django.db import models


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


class TelegramUser(models.Model):
    telegram_id = models.IntegerField(unique=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        if self.is_staff:
            status = 'Admin'
        else:
            status = 'User'
        return f"{status} {self.telegram_id}"


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
    category = models.ManyToManyField(Category, blank=True, null=True)
    brand = models.ManyToManyField(Brand, blank=True, null=True)
    subscribers = models.ManyToManyField(TelegramUser, blank=True, null=True)

    def __str__(self):
        return f'{self.pk}: {self.title}'


class TelegramText(models.Model):
    body = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
