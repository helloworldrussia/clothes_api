# Generated by Django 3.2.9 on 2022-11-27 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_alter_item_media_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='media_group',
            field=models.ManyToManyField(blank=True, related_name='media', to='items.MediaFile'),
        ),
    ]
