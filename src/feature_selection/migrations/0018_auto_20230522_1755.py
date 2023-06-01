# Generated by Django 3.2.13 on 2023-05-22 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feature_selection', '0017_clusterlabel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clusterlabel',
            name='trained_model',
        ),
        migrations.CreateModel(
            name='ClusterLabelsSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('trained_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cluster_labels', to='feature_selection.trainedmodel')),
            ],
        ),
        migrations.AddField(
            model_name='clusterlabel',
            name='cluster_label_set',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='feature_selection.clusterlabelsset'),
            preserve_default=False,
        ),
    ]
