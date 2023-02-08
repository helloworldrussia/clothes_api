# Generated by Django 3.2.9 on 2022-11-27 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_item_media_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='media_group',
            field=models.ManyToManyField(null=True, related_name='media', to='items.MediaFile'),
        ),
    ]