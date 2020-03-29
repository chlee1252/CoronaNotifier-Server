import sys
import requests
import csv

from datetime import datetime

sys.path.append("..")
from state.statename import createBaseDict, createDictList, states

base_url = 'https://facts.csbs.org/covid-19/covid19_county.csv'

def getCountyData():
  result = createBaseDict()

  request = requests.get(base_url)
  if request.status_code != 200:
    raise "REQUEST STATUS CODE EXCEPTION"
  
  text = request.text
  data = list(csv.DictReader(text.splitlines()))

  for item in data:
    state = item['State Name']
    county = item['County Name']

    if county == 'Unassigned' or county == 'Unknown' or state not in states:
      continue

    last_update = ' '.join(item['Last Update'].split(' ')[0:2])

    obj = {
      'County': county,
      'Confirmed': int(item['Confirmed']),
      'New Confirmed': int(item['New']),
      'Deaths': int(item['Death']),
      'New Death': int(item['New Death']),
      'Last Update': datetime.strptime(last_update, '%Y-%m-%d %H:%M').strftime("%m-%d-%Y %I:%M%p") + ' EDT',
    }

    result[state][county] = obj

  return result

def getDetailData():
  result = createDictList()
  request = requests.get(base_url)
  if request.status_code != 200:
    raise "REQUEST STATUS CODE EXCEPTION"
  
  text = request.text
  data = list(csv.DictReader(text.splitlines()))

  for item in data:
    state = item['State Name']
    county = item['County Name']

    if county == 'Unassigned' or county == 'Unknown' or state not in states:
      continue

    last_update = ' '.join(item['Last Update'].split(' ')[0:2])

    obj = {
      'County': county,
      'Confirmed': int(item['Confirmed']),
      'New Confirmed': int(item['New']),
      'Deaths': int(item['Death']),
      'New Death': int(item['New Death']),
      'Last Update': datetime.strptime(last_update, '%Y-%m-%d %H:%M').strftime("%m-%d-%Y %I:%M%p") + ' EDT',
    }

    result[state].append(obj)

  return result
