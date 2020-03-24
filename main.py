import os
import atexit

from flask import Flask, jsonify
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from county.county import getCountyData
from cache.cacheConfig import config
from state.state import getStateData

app = Flask(__name__)
cache = Cache()
config(app, cache)

@cache.cached(timeout=5, key_prefix='county')
def getCData():
  return 1

@cache.cached(timeout=5, key_prefix='state')
def getSData():
  return 2

sched = BackgroundScheduler(daemon=True)
sched.add_job(getCData,'interval', seconds=10)
sched.add_job(getSData,'interval', seconds=10)
sched.start()

@app.route('/')
def main():
  getCData()
  getSData()
  return "Welcome to CoronaNotifier API"
  
@app.route('/getCounty/<stateName>/<countyName>', methods=['GET'])
def getCounty(stateName, countyName):
  # data = cache.get('county')[stateName][countyName]
  return cache.get('county')

@app.route('/getState', methods=['GET'])
def getState():
  return cache.get('state')

atexit.register(lambda: sched.shutdown(wait=False))

if __name__=="__main__":
  port = int(os.environ.get('PORT', 5500))
  app.run(debug=True, host='0.0.0.0', port=port)
