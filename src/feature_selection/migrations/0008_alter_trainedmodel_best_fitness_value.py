# Generated by Django 3.2.13 on 2023-04-26 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_selection', '0007_auto_20230426_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainedmodel',
            name='best_fitness_value',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
