# Generated by Django 3.1.2 on 2022-05-12 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_service', '0049_auto_20211109_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='attempt',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
