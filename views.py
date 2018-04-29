from flask import Flask, render_template, request, session
from app import app
import uuid

@app.route('/debug')
def debug():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        babyScenario=scenarioMGR.getScenario(user_id)
        supplyList=babyScenario.supplyMGR.supplyList
        toReturn=[supply.pp for supply in supplyList if supply.available]
        return str(toReturn)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scenario')
def scenario():
    if 'user_id' in session.keys():
        return render_template('scenario.html')
    else:
        user_id=uuid.uuid4()
        scenarioMGR.getScenario(user_id)
        session['user_id']=user_id
        return render_template('scenario.html')

@app.route('/prepwarmer')
def prepwarmer():
    return render_template('prepwarmer.html')

@app.route('/resuscitation')
def resuscitation():
    return render_template('resuscitation.html')

@app.route('/getmodel', methods=["get", "post"])
def getmodel():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        babyScenario=scenarioMGR.getScenario(user_id)
        model_name=request.get_json()['model']
        getObject=getattr(babyScenario, model_name)
        toReturn=json.dumps(getObject.toJSON())
        return toReturn

@app.route('/updatedata', methods=["get", "post"])
def getUpdatedData():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        babyScenario=scenarioMGR.getScenario(user_id)
        supplyList=babyScenario.supplyMGR.supplyList
        PE=babyScenario.baby.PE
        app.logger.info([supply.pp for supply in babyScenario.supplyMGR.supplyList if supply.available])
        warmer=babyScenario.warmer
        returnDict={"PE":PE, "supplyList":supplyList, "warmer":warmer}
        toReturn=json.dumps(jsonclass.convertToJSON(returnDict))
        return toReturn

@app.route('/getscenario', methods=["get", "post"])
def getScenario():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        babyScenario=scenarioMGR.getScenario(user_id)
        toReturn=json.dumps(babyScenario.scenario_data)
        return toReturn

@app.route('/savedata', methods=["get", "post"])
def saveData():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        babyScenario=scenarioMGR.getScenario(user_id)
        model_name=request.get_json()['model_name']
        jsonModel=request.get_json()['model']
        model=getattr(babyScenario, model_name)
        model.setJSON(json.loads(jsonModel))
        return ""


@app.route('/doTask', methods=["post"])
def doTask():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        babyScenario=scenarioMGR.getScenario(user_id)
        taskName=request.get_json()['taskName']
        kv=request.get_json()['kv']
        babyScenario.tasks[taskName](**kv)
        return "success"