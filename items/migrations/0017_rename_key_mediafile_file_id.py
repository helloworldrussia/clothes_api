# Generated by Django 3.2.9 on 2022-12-12 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0016_auto_20221207_2128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediafile',
            old_name='key',
            new_name='file_id',
        ),
    ]
