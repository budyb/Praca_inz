# Generated by Django 2.2.4 on 2021-01-22 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0021_auto_20210122_1847'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistoricResults',
            new_name='HistoricResult',
        ),
        migrations.RenameModel(
            old_name='Results',
            new_name='Result',
        ),
    ]