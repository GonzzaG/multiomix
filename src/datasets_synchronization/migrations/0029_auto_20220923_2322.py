# Generated by Django 3.2.13 on 2022-09-23 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets_synchronization', '0028_auto_20210223_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cgdsdataset',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='cgdsstudy',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='survivalcolumnstuplecgdsdataset',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='survivalcolumnstupleuserfile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
