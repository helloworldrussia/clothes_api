# Generated by Django 3.2.9 on 2022-12-19 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0020_auto_20221218_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
