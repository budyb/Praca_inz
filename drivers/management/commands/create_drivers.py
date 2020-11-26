import re

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from drivers.models import Driver


class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            "https://www.formula1.com/en/drivers.html")
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")

        nameList = [i.text for i in soup.findAll("span", **{"class": "d-block f1--xxs f1-color--carbonBlack"})]
        surnameList = [i.text for i in soup.findAll("span", **{"class": "d-block f1-bold--s f1-color--carbonBlack"})]

        for name, surname in zip(nameList, surnameList):
            b = Driver(name=name, surname=surname)
            b.save()

            print(Driver(name=name, surname=surname))
