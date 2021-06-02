# Generated by Django 3.0.3 on 2020-05-20 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets_synchronization', '0012_auto_20200429_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cgdsstudy',
            name='state',
            field=models.IntegerField(choices=[(0, 'Unsynchronized'), (1, 'Waiting For Queue'), (2, 'In Process'), (3, 'Completed'), (4, 'Finished With Error'), (5, 'Url Error'), (6, 'Connection Timeout Error'), (7, 'Read Timeout Error')], default=0),
        ),
    ]
