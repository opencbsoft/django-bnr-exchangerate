import datetime
import requests
import xml.etree.ElementTree as ET
from decimal import Decimal, DecimalException

from django.core.management.base import BaseCommand

from bnr_exchangerate.models import ExchangeRate


class Command(BaseCommand):
    help = 'Download all the exchange rates from 2005 until today'

    def handle(self, **options):
        current_year = datetime.date.today().year
        self.stdout.write('Downloading all exchange rates from 2005 to {0}...'.format(current_year))
        days = 0
        for year in range(2005, current_year+1):
            url = 'http://www.bnr.ro/files/xml/years/nbrfxrates{0}.xml'.format(year)
            response = requests.get(url)
            root = ET.fromstring(response.text)
            for child in root[1]:
                if 'date' in child.attrib:
                    date = child.attrib['date']
                    for item in child:
                        currency = item.attrib['currency']
                        if 'multiplier' in item.attrib:
                            multiplier = item.attrib['multiplier']
                        else:
                            multiplier = 0
                        finish = True
                        try:
                            value = Decimal(item.text)
                        except:
                            finish = False
                        if finish:
                            try:
                                ExchangeRate.objects.create(currency=currency, value=value, date=date, multiplier=multiplier)
                            except:
                                pass
                            days += 1
        self.stdout.write('Process complete...imported {0} days.'.format(days))


