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

@cache.cached(timeout=0, key_prefix='county')
def getCData():
  cache.clear()
  return getCountyData()

@cache.cached(timeout=0, key_prefix='state')
def getSData():
  cache.clear()
  return getStateData()

sched = BackgroundScheduler(daemon=True)
sched.add_job(getCData,'interval', hours=1)
sched.add_job(getSData,'interval', hours=1)
sched.start()

@app.route('/')
def main():
  # getCData()
  # getSData()
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


atexit.register(lambda: sched.shutdown(wait=False))

if __name__=="__main__":
  port = int(os.environ.get('PORT', 5500))
  app.run(debug=True, host='0.0.0.0', port=port)
