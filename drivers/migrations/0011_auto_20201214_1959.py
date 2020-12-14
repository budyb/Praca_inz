# Generated by Django 2.2.4 on 2020-12-14 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0010_auto_20201214_1949'),
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