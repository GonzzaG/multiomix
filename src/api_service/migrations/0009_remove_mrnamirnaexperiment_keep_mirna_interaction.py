# Generated by Django 3.0.3 on 2020-04-09 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_service', '0008_auto_20200331_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mrnamirnaexperiment',
            name='keep_mirna_interaction',
        ),
    ]
