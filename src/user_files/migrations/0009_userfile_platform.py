# Generated by Django 3.0.3 on 2020-09-02 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_files', '0008_userfile_is_cg_site_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfile',
            name='platform',
            field=models.IntegerField(blank=True, choices=[(430, 'Platform 430')], null=True),
        ),
    ]
