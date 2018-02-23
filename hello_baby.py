from flask import Flask, render_template, request
import json
import sys
sys.path.append("/home/tukipenda/mysite/hello_baby_scenario")
from scenario import Scenario

app = Flask(__name__, static_url_path='/static')

#initializing scenario
babyScenario=Scenario()
babyScenario.loadData()


@app.route('/')
def home():
  return render_template('home.html')

@app.route('/scenario')
def scenario():
  return render_template('scenario.html')

@app.route('/prepwarmer')
def prepwarmer():
  return render_template('prepwarmer.html')

@app.route('/resuscitation')
def resuscitation():
  return render_template('resuscitation.html')

@app.route('/getmodel', methods=["get", "post"])
def getmodel():
    model_name=request.get_json()['model']
    getObject=getattr(babyScenario, model_name)
    toReturn=json.dumps(getObject.toJSON())
    return toReturn

@app.route('/getscenario', methods=["get", "post"])
def getScenario():
    toReturn=json.dumps(babyScenario.scenario_data)
    return toReturn

@app.route('/savedata', methods=["get", "post"])
def saveData():
    model_name=request.get_json()['model_name']
    jsonModel=request.get_json()['model']
    model=getattr(babyScenario, model_name)
    model.setJSON(json.loads(jsonModel))
    return ""