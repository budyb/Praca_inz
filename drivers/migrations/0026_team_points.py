# Generated by Django 2.2.4 on 2021-01-27 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0025_remove_prediction_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]