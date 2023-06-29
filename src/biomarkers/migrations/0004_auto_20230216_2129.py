# Generated by Django 3.2.13 on 2023-02-16 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biomarkers', '0003_auto_20230121_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='MRNAIdentifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=50)),
                ('biomarker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mrnas', to='biomarkers.biomarker')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='GeneIdentifier',
        ),
    ]
