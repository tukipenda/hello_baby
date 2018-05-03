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
        ppv.PPVCreateBaby(user)
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


@app.route('/dotask', methods=["post"])
def doTask():
    if 'user_id' in session.keys():
        user_id=session['user_id']
        user=models.User.query.filter_by(username=user_id).first()
        scenarioData=ppv.getScenarioData(user)
        return(json.dumps(scenarioData))