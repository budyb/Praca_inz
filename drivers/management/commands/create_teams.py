import re

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from drivers.models import Team


class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            "https://www.formula1.com/en/teams.html")
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
      
        nameList = [i.text for i in soup.findAll("span", **{"class": "f1-color--black"})]
        

        for name in nameList:
            name=name.replace(" ", "-")
            link="https://www.formula1.com/en/teams/" + name + ".html"
            r = requests.get(link)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "html.parser")
      
            data = [i.text for i in soup.findAll("td", **{"class": "stat-value"})]
            print(data)
            if not data:
                continue
            else:
                base = data.pop(1)
                chief = data.pop(1)
                tech_chief = data.pop(1)
                chassis = data.pop(1)
                pu_supplier = data.pop(1)
                first_entry = data.pop(1)
                world_champs = data.pop(1)
                highest_finisch = data.pop(1)
                pole_positions = data.pop(1)
                fastest_laps = data.pop(1)      
            b = Team(name=name, base=base, team_chief= chief, tech_chief=tech_chief, ch_producer=chassis,
             pu_supplier=pu_supplier, first_entry=first_entry, world_champs=world_champs ,highest_finisch=highest_finisch ,pole_positions=pole_positions ,fastest_laps=fastest_laps )
            b.save()


####https://www.formula1.com/content/dam/fom-website/teams/2020/ferrari.png -miniatura samochodu 