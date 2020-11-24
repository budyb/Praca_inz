import requests
import re
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from drivers.models import Schedule


class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            "https://www.formula1.com/en/racing/2020.html")
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")      
        data = soup.find("div",**{"class": "nav-list racing"})
        temp_links=str(data.findChildren("script"))
        temp_links=str(temp_links.split(":"))
        temp_links=temp_links.split('"')
        link_list=[]
        for link in temp_links:
            if "/content/fom-website/en/racing/2020/" in link:
                link_list.append(link)
            else:
                continue
        for link in link_list:
            link="https://www.formula1.com"+link
            link=link.replace(".html","/Timetable")+".html"
            print(link,"\n")
            r = requests.get(link)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "html.parser")      
            data = soup.find("div",**{"class": "table parbase"})
            table = data.tbody.find_all("tr")
            rows = []
            for row in table:
                row = row.text
                row = row.replace("\n",' ')
                row = row.replace('\xa0', ' ')
                rows.append(row)

            races = []   
            for row in rows:
                if "Formula 1" in row and ("Practice" in row or ("Qualifying " in row or "Grand Prix"in row)) and "Pit Stop" not in row:
                    races.append(row)
                    print(row,"\n")                    
                elif "SUNDAY" in row or "SATURDAY" in row or "FRIDAY" in row: 
                    races.append(row)
                    print(row,"\n")
                else:
                    pass
           
            # for dat in table_data:

            #     for td in table_data[table_data.index(dat)].find_all("td"):
            #         headings.append(td.text.strip())
            #rows = [data.tbody.findAll("Formula 1")]
            # for row in rows:
            #     print(row, "\n\n\n\n\n\n")

            
        
    


####https://www.formula1.com/content/dam/fom-website/teams/2020/ferrari.png -miniatura samochodu 