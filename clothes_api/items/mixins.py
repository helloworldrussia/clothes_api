from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class PageNumberSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = '-timestamp'
