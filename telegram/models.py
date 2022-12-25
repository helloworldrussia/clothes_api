from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.IntegerField(unique=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        if self.is_staff:
            status = 'Admin'
        else:
            status = 'User'
        return f"{status} {self.telegram_id}"


class TelegramText(models.Model):
    body = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name



