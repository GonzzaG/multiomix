# Generated by Django 3.0.3 on 2020-03-30 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_service', '0003_auto_20200317_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='mrnamirnaexperiment',
            name='type',
            field=models.IntegerField(choices=[(1, 'Mirna'), (2, 'Cnv'), (3, 'Methylation')], default=1),
            preserve_default=False,
        ),
    ]
