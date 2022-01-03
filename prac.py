
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
import configparser


cfg_name = "user.cfg"
cfg_section = "user_config"
config = configparser.ConfigParser()

if not os.path.exists(cfg_name):
    print("No configuration file (user.cfg) found! See README. Assuming default config...")
    config[cfg_section] = {}
else:
    config.read(cfg_name)

api_key = config.get(cfg_section, "coincap_api_key")

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
    "slug":["multi-chain-capital-new".lower(),],
}


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

quote = data["data"]["16160"]["quote"]
price = quote["USD"]["price"]

old_price = float("8.785991160407475e-05")
new_price = float("6.798904263091399e-05")

def get_change(current, previous):
    print(previous)
    print(current)
    if current == previous:
        return 100.0
    try:
        percentage_difference = (abs(current - previous) / previous) * 100.0
        percentage_difference_rounded = round(percentage_difference, 4)
        prefix  = "+" if current > previous else "-"
        output = f"{prefix}{str(percentage_difference_rounded)}"
        return output
    except ZeroDivisionError:
        return 0
    

print(get_change(old_price, new_price))
print(get_change(4,2))
print(get_change(2,4))
print(get_change(0.2,0.4))


def get_historical_price():
    session = Session()
    session.headers.update(headers)
    parameters={
        "id": "16160",
        "interval": "24h"
    }
    url= 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical'
    
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

get_historical_price()