from flask import Flask, render_template, request, session
from app import app, db
import uuid
import models
import preemie_ppv as ppv
import json
import preemie_ppv_update as ppv_update
import os


#need to adjust session safety - multiple tabs - have same id!

@app.route('/debug')
def debug():
    if 'user_id' in session.keys():
        pass

@app.route('/')
def home():
    session.clear()
    return render_template('home.html')

@app.route('/scenario')
def scenario():
    session['app_mode']='tutorial'
    #need to account for possibility that session has user_id, but user is not defined
    if 'user_id' in session.keys():
        return render_template('scenario.html')
    else:
        user_id=str(uuid.uuid4())
        session['user_id']=user_id
        user=models.User(username=user_id)
        db.session.add(user)
        db.session.commit()
        baby=ppv.PPVCreateBaby(user)
        session['baby_id']=baby.id
        return render_template('scenario.html')

@app.route('/prepwarmer')
def prepwarmer():
    session['app_mode']='tutorial'
    user_agent=request.headers.get('User-Agent')
    is_IE=False
    for test in ["msie", "trident", "edge"]:
        if test in user_agent.lower():
            is_IE=True
    return render_template('prepwarmer.html', is_IE=is_IE)

@app.route('/practice')
def practice():
    session['app_mode']='practice'
    user_agent=request.headers.get('User-Agent')
    is_IE=False
    for test in ["msie", "trident", "edge"]:
        if test in user_agent.lower():
            is_IE=True
    return render_template('prepwarmer.html', is_IE=is_IE)

@app.route('/exam')
def exam():
    session['app_mode']='exam'
    user_agent=request.headers.get('User-Agent')
    is_IE=False
    for test in ["msie", "trident", "edge"]:
        if test in user_agent.lower():
            is_IE=True
    return render_template('prepwarmer.html', is_IE=is_IE)


@app.route('/getscenario', methods=["get", "post"])
def getScenario():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        baby_id=session['baby_id'] # could be a source of bugs, need to watch
        time=request.get_json()['time']
        user=models.User.query.filter_by(username=user_id).first()
        if time>0:
            ub=ppv_update.UpdateBaby(baby_id)
            ub.update(time)
        scenarioData=ppv.getScenarioData(user)
        scenarioData['app_mode']=session['app_mode']
        return(json.dumps(scenarioData))
    else:
        return "" #ugh

@app.route('/updatewarmer', methods=["post"])
def updateWarmer():
    if 'baby_id' in session.keys():
        baby_id=session['baby_id']
        try:
            warmer_dict=json.loads(request.get_json()['warmer'])
            ppv.updateWarmer(baby_id, warmer_dict)
            return("")
        except:
            app.logger.info("warmer not a valid key")
            return ("error")
    else:
        return "baby unavailable" # this is so hacky!!

@app.route('/dotask', methods=["post"])
def doTask():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        baby_id=session['baby_id']
        time=request.get_json()['time']
        task=request.get_json()['task']
        taskName=task.pop('name')
        if 'supply_name' in task.keys():
            task['name']=task.pop('supply_name') #this is hacky too.
        if 'pp' in task.keys():
            task.pop('pp')
        ppv.doTask(baby_id, taskName, time, **task)
        return("")