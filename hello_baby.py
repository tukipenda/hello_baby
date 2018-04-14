from flask import Flask, render_template, request, session #learn to use flash?
from flask_debugtoolbar import DebugToolbarExtension
import json
import sys
sys.path.append("/home/tukipenda/mysite/hello_baby_scenario")
import jsonclass
from scenario import Scenario
from preemie_ppv import *
import uuid

app = Flask(__name__, static_url_path='/static')

#not secure
app.secret_key="something very easy"
app.debug=True

#toolbar = DebugToolbarExtension(app)

scenarioMGR=ScenarioMGR(PreemiePPVScenario)

@app.route('/debug')
def debug():
    return str(session['scenario_id'])

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
#        app.logger.info(model_name)
        toReturn=json.dumps(getObject.toJSON())
        return toReturn

@app.route('/updatedata', methods=["get", "post"])
def getUpdatedData():
    if 'scenario_id' in session.keys():
        scenario_id=session['scenario_id']
        babyScenario=scenarioMGR.getScenario(scenario_id)
        supplyList=babyScenario.supplyMGR.supplyList
        PE=babyScenario.baby.PE
        warmer=babyScenario.warmer
        app.logger.info(len([supply.name for supply in supplyList if supply.available]))
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
        app.logger.info(kv['name'])
        babyScenario.tasks[taskName](**kv)
        return "success"

if __name__=="__main__":
    s=scenarioMGR.getScenario(1)
    slist=s.supplyMGR.supplyList
    def getLen():
        alist=[supply.name for supply in slist if supply.available]
        print(len(alist))

    def fetch(num):
        k=slist[num]
        print(k.pp)
        size=""
        if not hasattr(k, "size"):
            size=None
        else:
            size=k.size
        s.tasks["fetch"](name=k.name, size=size)

    def pp():
        print([supply.name for supply in slist if supply.available])
