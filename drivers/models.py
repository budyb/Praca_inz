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
