from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.query import QuerySet
from django_group_by import GroupByMixin


class Driver(models.Model):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150, default="")
    nationality = models.CharField(
        max_length=150, default="No info", null=True)
    team = models.ForeignKey('Team', to_field='name',
                             null=True, on_delete=models.SET_NULL, related_name="driver")
    points = models.IntegerField(default=0)
    podiums = models.CharField(max_length=150, default="0", null=True)
    total_points = models.IntegerField(default=0, null=True)
    gp_entered = models.IntegerField(default=0, null=True)
    w_champs = models.CharField(max_length=150, default="0", null=True)
    highest_finish = models.CharField(max_length=150, default="", null=True)
    birthdate = models.DateField(null=True)
    number = models.IntegerField(default=0, null=True)

    def __str__(self):
        if self.nationality == None:
            self.nationality = "Brak danych"
        if self.podiums == None or self.podiums == "N/A":
            self.podiums = "0"
        if self.total_points == None or self.total_points == "N/A":
            self.total_points = "Brak danych"
        if self.gp_entered == None or self.gp_entered == "N/A":
            self.gp_entered = "Brak danych"
        if self.w_champs == None or self.w_champs == "N/A":
            self.w_champs = "0"
        if self.highest_finish == None or self.highest_finish == "N/A":
            self.highest_finish = "Brak danych"
        if self.birthdate == None or self.birthdate == "N/A":
            self.birthdate = "Brak danych"
        if self.number == None or self.number == "N/A":
            self.number = "Brak danych"
        return self.name + " " + self.surname

    


class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    points = models.IntegerField(default=0)
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

    def __str__(self):
        if self.first_entry == "N/A":
            self.first_entry = "Brak Danych"
        if self.world_champs == "N/A":
            self.world_champs = "0"
        if self.pole_positions == "N/A":
            self.pole_positions = "0"
        if self.fastest_laps == "N/A":
            self.fastest_laps = "0"
        return self.name


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

    def __str__(self):
        return self.full_name


class Ranking(models.Model):
    username = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, related_name="Rankings")
    points = models.IntegerField(default=0)


class Prediction(models.Model):
    first = models.ForeignKey('Driver', null=False,
                              on_delete=models.SET('%(class)s_Empty1'), related_name="Types_first")
    second = models.ForeignKey(
        'Driver', null=False, on_delete=models.SET('%(class)s_Empty2'), related_name="Types_second")
    third = models.ForeignKey('Driver', null=False,
                              on_delete=models.SET('%(class)s_Empty3'), related_name="Types_third")
    race = models.ForeignKey('Schedule', null=False,
                             on_delete=models.SET('%(class)s_EmptyR'), related_name="Types_race")
    ranking = models.ForeignKey(
        'Ranking', null=False, on_delete=models.CASCADE, related_name="Predictions")

class Season(models.Model):
    year = models.IntegerField(default = 1970)

    def __str__(self):
        return str(self.year)

class ResultQuerySet(QuerySet, GroupByMixin):
    pass

class Result(models.Model):
    objects = ResultQuerySet.as_manager()
    season = models.ForeignKey("Season", null=True, on_delete=models.SET_NULL)
    gp = models.ForeignKey("Schedule", default=0, null=False, on_delete=models.SET_DEFAULT, related_name="results")
    driver = models.ForeignKey("Driver", default="No info", null=False, on_delete=models.SET_DEFAULT)
    points = models.IntegerField(default=0)
    position = models.IntegerField(default = 20)

    def __str__(self):
        return self.gp.full_name

class HistoricResultQuerySet(QuerySet, GroupByMixin):
    pass
        
class HistoricResult(models.Model):
    objects = HistoricResultQuerySet.as_manager()
    season = models.ForeignKey("Season", null=True, on_delete=models.SET_NULL)
    gpName = models.CharField(max_length=350, null=False, default="No info")
    historicDriver = models.CharField(max_length = 350, null = False)
    hisPoints = models.IntegerField(default = 0)
    hisPosition = models.IntegerField(default = 20)

    def __str__(self):
        return self.gpName

