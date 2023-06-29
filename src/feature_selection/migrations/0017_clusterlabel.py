# Generated by Django 3.2.13 on 2023-05-16 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feature_selection', '0016_clusteringparameters_random_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=7)),
                ('cluster_id', models.IntegerField()),
                ('trained_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cluster_labels', to='feature_selection.trainedmodel')),
            ],
        ),
    ]
