from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Driver(models.Model):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150, default="")


class Team(models.Model):
    name = models.CharField(max_length=150)
    base = models.CharField(max_length=150)
    team_chief = models.CharField(max_length=150)
    tech_chief = models.CharField(max_length=150, null=True)
    ch_producer = models.CharField(max_length=150, null=True)
    pu_supplier = models.CharField(max_length=150, null=True)
    first_entry = models.CharField(max_length=4, null=True)
    world_champs = models.CharField(max_length=2, null=True)
    highest_finisch = models.CharField(max_length=2, null=True)
    pole_positions = models.CharField(max_length=3, null=True)
    fastest_laps = models.CharField(max_length=3, null=True)

class Schedule(models.Model):
    round_number = models.IntegerField()
    race = models.DateTimeField(null=False)
    quali = models.DateTimeField(null=False)
    fp3 = models.DateTimeField(null=True)
    fp2 = models.DateTimeField(null=True)
    fp1 = models.DateTimeField(null=True)
    country = models.CharField(max_length=150, null=False)
    full_name = models.CharField(max_length=250, null=False)
    circuit = models.CharField(max_length=150, null=False)
