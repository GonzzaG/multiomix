# Generated by Django 4.2.11 on 2024-05-31 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inferences', '0009_auto_20230922_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inferenceexperiment',
            name='state',
            field=models.IntegerField(choices=[(1, 'Completed'), (2, 'Finished With Error'), (3, 'In Process'), (4, 'Waiting For Queue'), (5, 'No Samples In Common'), (6, 'Stopping'), (7, 'Stopped'), (8, 'Reached Attempts Limit'), (9, 'No Features Found'), (10, 'Empty Dataset'), (11, 'No Valid Molecules'), (12, 'Number Of Samples Fewer Than Cv Folds'), (13, 'Timeout Exceeded')]),
        ),
    ]
