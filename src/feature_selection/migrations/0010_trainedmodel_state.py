# Generated by Django 3.2.13 on 2023-05-08 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_selection', '0009_auto_20230427_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainedmodel',
            name='state',
            field=models.IntegerField(choices=[(1, 'Completed'), (2, 'Finished With Error'), (3, 'In Process'), (4, 'Waiting For Queue'), (5, 'No Samples In Common'), (6, 'Stopping'), (7, 'Stopped'), (8, 'Reached Attempts Limit')], default=1),
            preserve_default=False,
        ),
    ]
