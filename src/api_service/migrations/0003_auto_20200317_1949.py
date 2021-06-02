# Generated by Django 3.0.3 on 2020-03-17 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_service', '0002_mrnamirnaexperiment_correlation_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='mrnamirnaexperiment',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mrnamirnaexperiment',
            name='name',
            field=models.CharField(default='viejo', max_length=30),
            preserve_default=False,
        ),
    ]
