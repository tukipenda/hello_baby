from flask import Flask, render_template, request, session #learn to use flash?
#from flask_debugtoolbar import DebugToolbarExtension
import json
import sys
sys.path.append("/home/tukipenda/mysite/hello_baby_scenario")
import jsonclass
from preemie_ppv import *
import uuid
import random

from scenario import Scenario
from preemie_ppv import *


app = Flask(__name__, static_url_path='/static')

#not secure
app.secret_key="something very easy"
app.debug=True

#toolbar = DebugToolbarExtension(app)

scenarioMGR=ScenarioMGR(PreemiePPVScenario)

@app.route('/debug')
def debug():
    if 'scenario_id' in session.keys():
        scenario_id=session['scenario_id']
        babyScenario=scenarioMGR.getScenario(scenario_id)
        supplyList=babyScenario.supplyMGR.supplyList
        toReturn=[supply.pp for supply in supplyList if supply.available]
        return str(toReturn)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scenario')
def scenario():
    if 'scenario_id' in session.keys():
        return render_template('scenario.html')
    else:
        scenario_id=uuid.uuid4()
        scenarioMGR.getScenario(scenario_id)
        session['scenario_id']=scenario_id
        return render_template('scenario.html')

@app.route('/prepwarmer')
def prepwarmer():
    return render_template('prepwarmer.html')

@app.route('/resuscitation')
def resuscitation():
    return render_template('resuscitation.html')

@app.route('/getmodel', methods=["get", "post"])
def getmodel():
    if 'scenario_id' in session.keys():
        scenario_id=session['scenario_id']
        babyScenario=scenarioMGR.getScenario(scenario_id)
        model_name=request.get_json()['model']
        getObject=getattr(babyScenario, model_name)
        toReturn=json.dumps(getObject.toJSON())
        return toReturn

@app.route('/updatedata', methods=["get", "post"])
def getUpdatedData():
    if 'scenario_id' in session.keys():
        scenario_id=session['scenario_id']
        babyScenario=scenarioMGR.getScenario(scenario_id)
        supplyList=babyScenario.supplyMGR.supplyList
        PE=babyScenario.baby.PE
        app.logger.info([supply.pp for supply in babyScenario.supplyMGR.supplyList if supply.available])
        warmer=babyScenario.warmer
        returnDict={"PE":PE, "supplyList":supplyList, "warmer":warmer}
        toReturn=json.dumps(jsonclass.convertToJSON(returnDict))
        return toReturn

@app.route('/getscenario', methods=["get", "post"])
def getScenario():
    if 'scenario_id' in session.keys():
        scenario_id=session['scenario_id']
        babyScenario=scenarioMGR.getScenario(scenario_id)
        toReturn=json.dumps(babyScenario.scenario_data)
        return toReturn

@app.route('/savedata', methods=["get", "post"])
def saveData():
    if 'scenario_id' in session.keys():
        scenario_id=session['scenario_id']
        babyScenario=scenarioMGR.getScenario(scenario_id)
        model_name=request.get_json()['model_name']
        jsonModel=request.get_json()['model']
        model=getattr(babyScenario, model_name)
        model.setJSON(json.loads(jsonModel))
        return ""


@app.route('/doTask', methods=["post"])
def doTask():
    if 'scenario_id' in session.keys():
        scenario_id=session['scenario_id']
        babyScenario=scenarioMGR.getScenario(scenario_id)
        taskName=request.get_json()['taskName']
        kv=request.get_json()['kv']
        babyScenario.tasks[taskName](**kv)
        return "success"

if __name__=="__main__":
    s=scenarioMGR.getScenario(1)
    slist=s.supplyMGR.supplyList