import requests
import re
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from datetime import datetime
from drivers.models import Schedule



class Command(BaseCommand):

    def handle(self, *args, **options):
        #Schedule.objects.all().delete()
        r = requests.get(
            "https://www.formula1.com/en/racing/2020.html")
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")      
        data = str(soup.findAll("div",**{"class": "col-12 col-sm-6 col-lg-4 col-xl-3"}))
        temp_links = data.split(" ")
        # temp_links=str(data.findChildren("script"))
        # temp_links=str(temp_links.split(":"))
        # temp_links=temp_links.split('"')
        link_list=[]
        for link in temp_links:
            if "/en/racing/2020/" in link and "Test" not in link:
                link = link.replace("<fieldset","")
                link = link.replace('href="',"")
                link = link.replace('">\n',"")
                link_list.append(link)        
            else:
                continue
        
        i=0
        for link in link_list:
            link="https://www.formula1.com"+link
            print(link)
            r = requests.get(link)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "html.parser")      
            country = soup.find("h1",**{"class": "race-location f1-bold--xxl f1-uppercase f1-color--white no-margin"}).text.replace("2020","")
            full_name = soup.find("h2",**{"class": "f1--s"}).text
            circuit = soup.find("p",**{"class": "f1-uppercase misc--tag no-margin"}).text
            race = str(soup.find("div",**{"class": "row js-race"})).split(" ")[5].replace('>\n<div',"").replace('"'," ")
            zone = str(soup.find("div",**{"class": "row js-race"})).split(" ")[4].replace('>\n<div',"").replace('data-gmt-offset=',"").replace('"',"")
            print(zone)
            quali = str(soup.find("div",**{"class": "row js-qualifying"})).split(" ")[5].replace('>\n<div',"").replace('"'," ")
            fp3 = str(soup.find("div",**{"class": "row js-practice-3"})).split(" ")
            fp2 = str(soup.find("div",**{"class": "row js-practice-2"})).split(" ")
            fp1 = str(soup.find("div",**{"class": "row js-practice-1"})).split(" ")
            if ((fp1==['None']) or ('data-override-status="CANCELLED"' in fp1)):
                fp1=None
            else:
                fp1=fp1[5].replace('>\n<div',"").replace('"'," ")
                fp1 = fp1 + zone
                fp1 = datetime.strptime(fp1, 'data-start-time= %Y-%m-%dT%H:%M:%S %z')

            if ((fp2==['None']) or ('data-override-status="CANCELLED"' in fp2)):
                fp2=None
            else:
                fp2=fp2[5].replace('>\n<div',"").replace('"'," ")
                fp2 = fp2 + zone
                fp2 = datetime.strptime(fp2, 'data-start-time= %Y-%m-%dT%H:%M:%S %z')

            if ((fp3==['None']) or ('data-override-status="CANCELLED"' in fp3)):
                fp3=None
            else: 
                fp3=fp3[5].replace('>\n<div',"").replace('"'," ")
                fp3 = fp3 + zone
                fp3 = datetime.strptime(fp3, 'data-start-time= %Y-%m-%dT%H:%M:%S %z')   

            race = race + zone
            quali = quali + zone
            print(race, "\n")          
            race = datetime.strptime(race, 'data-start-time= %Y-%m-%dT%H:%M:%S %z')
            quali = datetime.strptime(quali, 'data-start-time= %Y-%m-%dT%H:%M:%S %z')
            b = Schedule(round_number=i, race=race, quali=quali, fp3=fp3, fp2=fp2, fp1=fp1, country=country, full_name=full_name, circuit=circuit)
            b.save()
            i += 1