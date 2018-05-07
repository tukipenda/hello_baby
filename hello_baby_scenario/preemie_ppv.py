import models
from models import db
from app import app
import json
import preemie_ppv_data as data
import preemie_ppv_update as ppv_update
from preemie_ppv_update import getSubDict, getSupplies

baby_data=json.dumps(data.baby_data)
mom_data=json.dumps(data.mom_data)
baby_PE=json.dumps(data.PE)
supplies=json.dumps(data.supplyList)
warmer=json.dumps(data.warmer)
tasks=json.dumps(data.tasks)
vent=json.dumps(data.vent)
cpr=json.dumps(data.cpr)
uvc=json.dumps(data.uvc)
health=json.dumps(data.health)
ppvScenario=models.Scenario(name="preemie_ppv", scenario=data.scenario, baby_data=baby_data, mom_data=mom_data, baby_PE=baby_PE, supplies=supplies, warmer=warmer, tasks=tasks, vent=vent, cpr=cpr, uvc=uvc, health=health)
db.session.add(ppvScenario)
db.session.commit()

def PPVCreateBaby(user):
    ppvScenario=models.Scenario.query.filter_by(name="preemie_ppv").first()
    return models.create_baby(user, ppvScenario)

def getScenarioData(user):
    scenario=models.Scenario.query.filter_by(name="preemie_ppv").first()
    baby=models.Baby.query.filter_by(user_id=user.id).first()
    babyDict=getSubDict(baby.__dict__, data.baby_data.keys())
    PE={}
    for e, m in models.PEDict.items():
        result=m.query.filter_by(baby_id=baby.id).first()
        PE[e]=getSubDict(result.__dict__, data.PE[e].keys())
    warmer=models.Warmer.query.filter_by(baby_id=baby.id).first()
    warmer=getSubDict(warmer.__dict__, data.warmer.keys())
    scenario_text=scenario.scenario
    mom=json.loads(scenario.mom_data)
    tasks=json.loads(scenario.tasks)
    returnDict={
        'scenario_text':scenario_text,
        'PE':PE,
        'mom':mom,
        'baby':babyDict,
        'warmer':warmer,
        'supplies':getSupplies(baby.id),
        'tasks': tasks
    }
    return returnDict

def updateWarmer(baby_id, warmer_dict):
    models.Warmer.query.filter_by(baby_id=baby_id).update(warmer_dict)
    db.session.commit()
    warmer=models.Warmer.query.filter_by(baby_id=baby_id).first()

def doTask(ub, baby_id, taskName, time, **kwargs):
    task=ppv_update.taskDict[taskName]
    task(baby_id, **kwargs)
    db.session.commit()
    ub.update(time)


