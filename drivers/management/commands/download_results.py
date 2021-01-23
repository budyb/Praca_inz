import requests
import re
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from datetime import datetime
from drivers.models import *



class Command(BaseCommand):

    def handle(self, *args, **options):
        races = Schedule.objects.all()
        drivers = Driver.objects.all()
        year = "1950"
        Historic = False
        if int(year) < 2020:
            Historic = True
        good_race = ''

        r = requests.get(
            "https://www.formula1.com/en/results.html/"+year+"/races.html")
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")      
        data = str(soup.findAll("td",**{"class": "dark bold"}))
        temp_links = data.split(" ")
        link_list=[]
        for link in temp_links:
            if "href" in link :
                link = link.replace("<fieldset","")
                link = link.replace('href="',"")
                link = link.replace('">\n',"")
                link="https://www.formula1.com"+link
                link_list.append(link)        
            else:
                continue
        for link in link_list:
            print(link)
            r = requests.get(link)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "html.parser")  

            data = str(soup.findAll("span",**{"class": "full-date"})).replace('[<span class="full-date">',"")
            data = data.replace('</span>]',"")
            data = datetime.strptime(data, "%d %b %Y").date()
            race_name = soup.find("h1",**{"class": "ResultsArchiveTitle"})
            race_name = race_name.text.replace("- RACE RESULT","").strip()

            seasons = Season.objects.all()
            season = ''
            gp = ''
            found_season = False
            
            if not seasons:
                season = Season(year=year)
                season.save()
                found_season = True
            else:
                for sez in seasons:
                    if sez.year == int(year):
                        season = sez
                        found_season = True
                    else:
                        continue
            if not found_season:
                season=Season(year=year)
                season.save()

            rows = soup.find("tbody")            
            rows = rows.findAll("tr")
            
            current_position=0
            for row in rows:
                row_splited=row.text.split("\n")
                current_position +=1
                position = row_splited[2]
                name = row_splited[5]
                surname = row_splited[6]
                points = row_splited[12]
                if not position.isnumeric():
                    position = str(current_position)
                
                if not Historic:
                    for gp in races:
                        if gp.race.date() == data:
                            good_race = gp
                        else:
                            continue
                    driver = ''
                    for driv in drivers:
                        if driv.surname == surname:
                            driver = driv                        
                        else:
                            continue
                    result = Result(season = season, gp=good_race, driver=driver, points=points, position=position)
                    result.save()                    
                else:
                    hist_result = HistoricResult(season=season, gpName=race_name, historicDriver=name+ " "+ surname, hisPoints=points, hisPosition=position)
                    hist_result.save()

                