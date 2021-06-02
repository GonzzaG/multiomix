# Generated by Django 3.1.2 on 2020-12-28 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets_synchronization', '0022_auto_20200903_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cgdsstudy',
            name='state',
            field=models.IntegerField(choices=[(0, 'Not Synchronized'), (1, 'Waiting For Queue'), (2, 'In Process'), (3, 'Completed'), (4, 'Finished With Error'), (5, 'Url Error'), (6, 'Connection Timeout Error'), (7, 'Read Timeout Error')], default=0),
        ),
    ]
