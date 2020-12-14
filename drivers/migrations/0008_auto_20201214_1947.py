# Generated by Django 2.2.4 on 2020-12-14 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0007_auto_20201214_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='drivers.Team', to_field='name'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
