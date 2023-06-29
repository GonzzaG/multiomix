# Generated by Django 3.2.13 on 2023-04-26 22:22

from django.db import migrations, models
import django.db.models.deletion


def remove_all_model_parameters(apps, schema_editor):
    """Removes all the ClusteringParameters and SVMParameters to prevents error due to DB's structure modification."""
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    ClusteringParameters = apps.get_model("feature_selection", "ClusteringParameters")
    SVMParameters = apps.get_model("feature_selection", "SVMParameters")

    ClusteringParameters.objects.all().delete()
    SVMParameters.objects.all().delete()



class Migration(migrations.Migration):

    dependencies = [
        ('feature_selection', '0006_auto_20230417_1930'),
    ]

    operations = [
        migrations.RunPython(remove_all_model_parameters),
        migrations.RemoveField(
            model_name='clusteringparameters',
            name='experiment',
        ),
        migrations.RemoveField(
            model_name='fsexperiment',
            name='fitness_function',
        ),
        migrations.RemoveField(
            model_name='svmparameters',
            name='experiment',
        ),
        migrations.AddField(
            model_name='clusteringparameters',
            name='trained_model',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='clustering_parameters', to='feature_selection.trainedmodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='svmparameters',
            name='trained_model',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='svm_parameters', to='feature_selection.trainedmodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainedmodel',
            name='fitness_function',
            field=models.IntegerField(choices=[(1, 'Clustering'), (2, 'Svm'), (3, 'Rf')], default=1),
            preserve_default=False,
        ),
    ]
