import datetime
import requests
import xml.etree.ElementTree as ET
from decimal import Decimal, DecimalException

from django.core.management.base import BaseCommand

from bnr_exchangerate.models import ExchangeRate


class Command(BaseCommand):
    help = 'Download all the exchange rates from 2005 until today'

    def handle(self, **options):
        self.stdout.write('Get the daily exchange rates...')
        url = 'http://www.bnr.ro/nbrfxrates.xml'
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
                    value = Decimal(item.text)
                    ExchangeRate.objects.create(currency=currency, value=value, date=date, multiplier=multiplier)
        self.stdout.write('Process complete.')


