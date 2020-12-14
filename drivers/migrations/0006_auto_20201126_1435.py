# Generated by Django 2.2.4 on 2020-11-26 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0005_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='nationality',
            field=models.CharField(default='No info', max_length=150),
        ),
        migrations.AddField(
            model_name='driver',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='driver',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='drivers.Team'),
        ),
    ]
