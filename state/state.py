import requests
import csv
from datetime import datetime
import urllib.request, json 
import dateutil.parser

# from .statename import createBaseDict, states

# def getStateData():
#   base_url = 'https://facts.csbs.org/covid-19/covid19_state.csv'
#   result = []

#   request = requests.get(base_url)
#   if request.status_code != 200:
#     raise "REQUEST STATUS CODE EXCEPTION"

#   text = request.text
#   data = list(csv.DictReader(text.splitlines()))
#   total_confirmed = 0
#   total_newConfirmed = 0
#   total_Deaths = 0
#   total_newDeaths = 0
#   lastTotal = None

#   for item in data:
#     state = item['State Name']
    
#     if state not in states:
#       continue
    
#     last_update = ' '.join(item['Last Update'].split(' ')[0:2])
#     confirm = int(item['Confirmed'])
#     newConfirm = int(item['New'])
#     deaths = int(item['Death'])
#     newDeaths = int(item['New Death'])
#     last = datetime.strptime(last_update, '%Y-%m-%d %H:%M').strftime("%m-%d-%Y %I:%M%p") + ' EDT'
#     obj = {
#       'state': state,
#       'Confirmed': confirm,
#       'New Confirmed': newConfirm,
#       'Deaths': deaths,
#       'New Death': newDeaths,
#       'Last Update': last,
#     }
#     total_confirmed += confirm
#     total_newConfirmed += newConfirm
#     total_Deaths += deaths
#     total_newDeaths += newDeaths
#     lastTotal = last

#     result.append(obj)
  
#   total_obj = {
#       'state': 'US (Mainland)',
#       'Confirmed': total_confirmed,
#       'New Confirmed': total_newConfirmed,
#       'Deaths': total_Deaths,
#       'New Death': total_newDeaths,
#       'Last Update': lastTotal,
#     }
#   result.insert(0, total_obj)


#   return result

def getTimeline():
  uri = 'https://coronavirus-tracker-api.herokuapp.com/v2/locations/225'
  obj = {'US': []}
  with urllib.request.urlopen(uri) as url:
    data = json.loads(url.read().decode())
    
    affected = data['location']['timelines']['confirmed']['timeline']
    death = data['location']['timelines']['deaths']['timeline']
    
    result = obj['US']
    keys = list(affected.keys())[-60:]
    for key in keys:
      newkey = dateutil.parser.isoparse(key).strftime('%m/%d/%y')
      result.append({
        'date': newkey,
        'affected': affected[key],
        'deaths': death[key]
      })
  return obj
