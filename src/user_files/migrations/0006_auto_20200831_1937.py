# Generated by Django 3.0.3 on 2020-08-31 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_files', '0005_auto_20200827_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfile',
            name='column_used_as_index',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userfile',
            name='contains_nan_values',
            field=models.BooleanField(default=False),
        ),
    ]
