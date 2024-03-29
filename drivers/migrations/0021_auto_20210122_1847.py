# Generated by Django 2.2.4 on 2021-01-22 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0020_auto_20210121_0023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicgp',
            name='season',
        ),
        migrations.RemoveField(
            model_name='historicresults',
            name='historicRace',
        ),
        migrations.RemoveField(
            model_name='results',
            name='race',
        ),
        migrations.AddField(
            model_name='historicresults',
            name='gpName',
            field=models.CharField(default='No info', max_length=350),
        ),
        migrations.AddField(
            model_name='historicresults',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='drivers.Season'),
        ),
        migrations.AddField(
            model_name='results',
            name='gp',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='results', to='drivers.Schedule'),
        ),
        migrations.AddField(
            model_name='results',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='drivers.Season'),
        ),
        migrations.DeleteModel(
            name='GP',
        ),
        migrations.DeleteModel(
            name='HistoricGP',
        ),
    ]
