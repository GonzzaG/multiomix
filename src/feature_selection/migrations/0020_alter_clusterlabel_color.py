# Generated by Django 3.2.13 on 2023-05-22 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_selection', '0019_alter_clusterlabel_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clusterlabel',
            name='color',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
