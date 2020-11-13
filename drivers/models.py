from django.db import models
from django.contrib.auth.models import User


class Driver(models.Model):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150, default="")


# class User(models.Model):
#     login = models.CharField(User, max_length=50)
#     password = models.CharField(max_length=50)
