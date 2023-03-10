# Generated by Django 3.2.9 on 2022-11-27 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0012_auto_20221127_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='brand',
        ),
        migrations.AddField(
            model_name='item',
            name='brand',
            field=models.ManyToManyField(blank=True, null=True, to='items.Brand'),
        ),
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='items.Category'),
        ),
        migrations.RemoveField(
            model_name='item',
            name='media_group',
        ),
        migrations.AddField(
            model_name='item',
            name='media_group',
            field=models.ManyToManyField(blank=True, null=True, to='items.MediaFile'),
        ),
    ]
