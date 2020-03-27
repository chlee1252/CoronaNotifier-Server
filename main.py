import os
import atexit

from pytz import utc
from flask import Flask, jsonify
# from datetime import datetime
from flask_caching import Cache
# from apscheduler.schedulers.background import BackgroundScheduler
from county.county import getCountyData
from cache.cacheConfig import config
from state.state import getStateData


# TODO: Pagination on State

app = Flask(__name__)
cache = Cache()
config(app, cache)

# sched = BackgroundScheduler(timezone=utc)
# date = datetime.today()
# newdate = date.replace(hour=2, minute=12, second=0)
# print(newdate)

# Delete Cache after 45 minutes
@cache.cached(timeout=(60*30), key_prefix='county')
# @sched.scheduled_job('interval', minutes=1, next_run_time=newdate)
def getCData():
  cache.clear()
  return getCountyData()

@cache.cached(timeout=(60*30), key_prefix='state')
# @sched.scheduled_job('interval', minutes=1, next_run_time=newdate)
def getSData():
  cache.clear()
  return getStateData()

@app.route('/')
def main():
  getCData()
  getSData()
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
  return jsonify(cache.get('state'))

@app.route('/getTimeHistory/<stateName>/<countyName>', methods=['GET'])
def getTimeHistory(stateName, countyName):
  return "This is TimeHistory Panel: Not Implemented."

@app.route('/getStateDetail/<stateName>')
def getStateDetail(stateName):
    if not cache.get('county'):
      getCData()
    return jsonify(cache.get('county')[stateName])

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
