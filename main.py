import os
import atexit

from pytz import utc
from flask import Flask, jsonify
from datetime import datetime
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from county.county import getCountyData
from cache.cacheConfig import config
from state.state import getStateData

app = Flask(__name__)
cache = Cache()
config(app, cache)

sched = BackgroundScheduler(timezone=utc)
date = datetime.today()
newdate = date.replace(hour=2, minute=2, second=10)

@cache.cached(timeout=0, key_prefix='county')
@sched.scheduled_job('interval', hours=1, next_run_time=newdate)
def getCData():
  cache.clear()
  return getCountyData()

@cache.cached(timeout=0, key_prefix='state')
@sched.scheduled_job('interval', hours=1, next_run_time=newdate)
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
  data = cache.get('county')[stateName][countyName]
  return jsonify(data)

@app.route('/getState', methods=['GET'])
def getState():
  if not cache.get('state'):
    getSData()

  return jsonify(cache.get('state'))

@app.route('/clearCache')
def clearCache():
  cache.clear()
  return "Done"

# atexit.register(lambda: sched.shutdown(wait=False))

if __name__=="__main__":
  port = int(os.environ.get('PORT', 5500))
  app.run(debug=True, host='0.0.0.0', port=port)
