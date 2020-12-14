import re

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from unidecode import unidecode
from datetime import datetime
from drivers.models import Driver, Team


# class Command(BaseCommand):

#     def handle(self, *args, **options):
#         r = requests.get(
#             "https://www.formula1.com/en/drivers.html")
#         r.encoding = r.apparent_encoding
#         soup = BeautifulSoup(r.text, "html.parser")

#         nameList = [i.text for i in soup.findAll("span", **{"class": "d-block f1--xxs f1-color--carbonBlack"})]
#         surnameList = [i.text for i in soup.findAll("span", **{"class": "d-block f1-bold--s f1-color--carbonBlack"})]
        

#         for name, surname in zip(nameList, surnameList):
#             b = Driver(name=name, surname=surname)
#             b.save()

#             print(Driver(name=name, surname=surname))

class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            "https://www.formula1.com/en/drivers.html")
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html.parser")

        Driver.objects.all().delete()
        teams = Team.objects.all()
        nameList = [i.text for i in soup.findAll("span", **{"class": "d-block f1--xxs f1-color--carbonBlack"})]
        surnameList = [i.text for i in soup.findAll("span", **{"class": "d-block f1-bold--s f1-color--carbonBlack"})]
        pointsList = [i.text for i in soup.findAll("div", **{"class": "f1-wide--s"})]
        teamsList = [i.text for i in soup.findAll("p", **{"class": "listing-item--team f1--xxs f1-color--gray5"})]
        
        for name,surname, points, squad in zip(nameList, surnameList, pointsList, teamsList):
            surname_link = unidecode(surname)
            name_link = unidecode(name)
            
            link = "https://www.formula1.com/en/drivers/" + name_link.lower() + "-" + surname_link.lower() + ".html"
            r = requests.get(link)
           
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "html.parser")
            
            name = soup.find("h1", **{"class": "driver-name"})
            number = soup.find("div", **{"class": "driver-number"})
            squad = squad.replace(" ",  "-")
            team = Team((),{})
            for te in teams:
                if(te.name==squad):
                    team=te
                    print(team.name)
                else:
                    continue

            if name is not None:
                number=number.text.strip()
                name = name.text.split(" ")

                List = [i.text for i in soup.findAll("td", **{"class": "stat-value"})]
                country = List[1]
                podiums = List[2]
                total_points = List[3]
                gp_entered = List[4]
                w_champs = List[5]
                highest_finish = List[6]
                birthdate = datetime.strptime(List[8], "%d/%m/%Y").date()
            else:
                name = [name_link , surname_link]
                country = None
                podiums = None
                total_points = None
                gp_entered = None
                highest_finish = None
                birthdate = None
                w_champs = None
  
            b = Driver(name=name[0], surname=name[1], points=points, nationality=country, team=team, number=number, podiums=podiums,
             total_points=total_points, gp_entered=gp_entered, w_champs=w_champs, highest_finish=highest_finish, birthdate=birthdate)
            b.save()
            

        
