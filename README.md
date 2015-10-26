# django-bnr-exchangerate
A django application that handles the updating and supplying of an exchange rate. It was tested with Django 1.8+ and Python 3.4
## Instalation
```
pip install django-bnr-exchangerate
```
Add to settings.py
```
'bnr_exchangerate',
```
## Example usage
Get an exchange rate for a value for a certain day.
If the day is on saturday or on sunday it will automatically get the friday exchange rate
```
from bnr_exchangerate.models import ExchangeRate
value = ExchangeRate.get_rate('EUR', '2015-10-10')
```
To import the history from 2005 to current year into the database execute the following command
```
./manage.py get_history
```
To update daily exchange rate run the following command
```
./manage.py get_daily
```