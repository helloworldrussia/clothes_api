# Generated by Django 3.2.9 on 2022-12-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0022_auto_20221223_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramtext',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
