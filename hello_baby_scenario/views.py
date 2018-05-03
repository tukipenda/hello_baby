from flask import Flask, render_template, request, session
from app import app, db
import uuid
import models
import preemie_ppv as ppv
import json

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
    return render_template('prepwarmer.html')


@app.route('/getscenario', methods=["get", "post"])
def getScenario():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        user=models.User.query.filter_by(username=user_id).first()
        scenarioData=ppv.getScenarioData(user)
        return(json.dumps(scenarioData))

@app.route('/updatewarmer', methods=["post"])
def updateWarmer():
    if 'baby_id' in session.keys():
        baby_id=session['baby_id']
        warmer_dict=request.get_json()['warmer']
        ppv.updateWarmer(baby_id, warmer_dict)
        return("")

@app.route('/dotask', methods=["post"])
def doTask():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        baby_id=session['baby_id']
        taskName=request.get_json()['name']
        kwargs=request.get_json()['kwargs']
        ppv.doTask(baby_id, taskName, **kwargs)
        return("")