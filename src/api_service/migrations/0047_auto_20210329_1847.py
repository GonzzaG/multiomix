# Generated by Django 3.1.2 on 2021-03-29 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_service', '0046_auto_20210121_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='clinical_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clinical_source', to='api_service.experimentclinicalsource'),
        ),
    ]
