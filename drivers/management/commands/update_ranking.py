from django.core.management import BaseCommand
from datetime import datetime
from drivers.models import Ranking, Prediction, Result, Season, Schedule


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='Season represented by year')
        parser.add_argument('race', type=str, help='GrandPrix full name' )

    def handle(self, *args, **options):
        year = options['year']
        r_name = options['race']
        season = Season.objects.get(year=year)
        gp = Schedule.objects.get(full_name=r_name)
        first = Result.objects.get(season=season, gp=gp, position=1).driver
        second = Result.objects.get(season=season, gp=gp, position=2).driver
        third = Result.objects.get(season=season, gp=gp, position=3).driver
        
        points_for3 = 20
        points_for2 = 15
        points_for1 = 10
        bonus = 5
        rankings = Ranking.objects.all()
        for ranking in rankings:
            correct_positions = [False, False, False]
            result_drivers = [first, second, third]
            prediction = ranking.Predictions.get(race=gp)
            if prediction.first == first:
                correct_positions[0] = True
            if prediction.second == second:
                correct_positions[1] = True
            if prediction.third == third:
                correct_positions[2] = True
            if prediction.first in result_drivers and prediction.second in result_drivers and prediction.third in result_drivers:
                ranking.points += bonus
            if sum(correct_positions) == 3:
                ranking.points += points_for3
            elif sum(correct_positions) == 2:
                ranking.points += points_for2
            elif sum(correct_positions) == 1:
                ranking.points += points_for1
            
            ranking.save()
        
        