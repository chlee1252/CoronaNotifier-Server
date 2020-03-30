import os
import atexit

from pytz import utc
from flask import Flask, request, jsonify
# from datetime import datetime
from flask_caching import Cache
# from apscheduler.schedulers.background import BackgroundScheduler
from county.county import getCountyData, getDetailData
from cache.cacheConfig import config
from state.state import getStateData, getTimeline
from pagination.pagination import getPaginatedList


# TODO: Pagination on State

app = Flask(__name__)
cache = Cache()
config(app, cache)
app.config['JSON_SORT_KEYS'] = False

# sched = BackgroundScheduler(timezone=utc)
# date = datetime.today()
# newdate = date.replace(hour=2, minute=12, second=0)
# print(newdate)

# Delete Cache after 30 minutes
@cache.cached(timeout=(60*30), key_prefix='county')
# @sched.scheduled_job('interval', minutes=1, next_run_time=newdate)
def getCData():
  cache.delete('county')
  try:
    return getCountyData() 
  except:
    return None

@cache.cached(timeout=(60*30), key_prefix='state')
# @sched.scheduled_job('interval', minutes=1, next_run_time=newdate)
def getSData():
  cache.delete('state')
  try:
      return getStateData()
  except:
    return None

@cache.cached(timeout=(60*30), key_prefix='dataForCountyPage')
def getCDData():
  cache.delete('dataForCountyPage')
  return getDetailData()

@cache.cached(timeout=(60*30), key_prefix='timeline')
def getTimeHistory():
  cache.delete('timeline')
  return getTimeline()

@app.route('/')
def main():
  getCData()
  getSData()
  getCData()
  getTimeHistory()
  return "Welcome to CoronaNotifier API"
  
@app.route('/getCounty/<stateName>/<countyName>', methods=['GET'])
def getCounty(stateName, countyName):
  if not cache.get('county'):
    getCData()
  data = cache.get('county')[stateName]
  return jsonify(data[countyName]) if countyName in data else jsonify(None)

@app.route('/getState', methods=['GET'])
def getState():
  if not cache.get('state'):
    getSData()
  # data = cache.get('state') # pageination code
  # return jsonify(getPaginatedList(
  #   data, 
  #   '/getState', 
  #   start=request.args.get('start'), 
  #   limit=request.args.get('limit')
  #   )
  # )
  return jsonify(cache.get('state'))

@app.route('/getTimeHistory', methods=['GET'])
def getTime():
  if not cache.get('timeline'):
    getTimeHistory()
  return jsonify(cache.get('timeline'))

@app.route('/getStateDetail/<stateName>')
def getStateDetail(stateName):
    if not cache.get('dataForCountyPage'):
      getCDData()
    data = cache.get('dataForCountyPage')
    
    # return jsonify(
    #   getPaginatedList(
    #     data[stateName],
    #     '/getStateDetail/%s' % stateName,
    #     start=request.args.get('start'),
    #     limit=request.args.get('limit')
    #   )
    # )
    return jsonify(data[stateName])

@app.route('/get30Day')
def get30DayData():
  return

@app.route('/clearCache')
def clearCache():
  cache.clear()
  return "Done"

@app.route('/getCache')
def getCache():
  return jsonify(cache.get('state'))

# atexit.register(lambda: sched.shutdown(wait=False))

if __name__=="__main__":
  port = int(os.environ.get('PORT', 5500))
  app.run(debug=True, host='0.0.0.0', port=port)
