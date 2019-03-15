import models
from models import db
from app import app
import json
import preemie_ppv_data as data
import preemie_ppv_update as ppv_update
from preemie_ppv_update import getSubDict, getSupplies
import pretty_print_baby as ppb

value_list=['baby_data', 'scenario', 'history', 'PE', 'supplies', 'warmer', 'tasks', 'vent', 'cpr', 'uvc', 'health']
scenarioDict={name:json.dumps(getattr(data, name)) for name in value_list}
ppvScenario=models.Scenario(name="preemie_ppv", **scenarioDict)

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
    resusc={}
    for r, m in models.resuscDict.items():
        if r!="health":
            result=m.query.filter_by(baby_id=baby.id).first()
            resusc[r]=getSubDict(result.__dict__, getattr(data, r).keys())
    warmer=models.Warmer.query.filter_by(baby_id=baby.id).first()
    warmer=getSubDict(warmer.__dict__, data.warmer.keys())
    scenario_text=json.loads(scenario.scenario)
    history=json.loads(scenario.history)
    tasks=json.loads(scenario.tasks)
    
    a=models.Actionlog().query.filter_by(baby_id=baby.id).first()
    app.logger.info(a)
    actionLog=[]
    for action in a.actions:
        actionLog.append({'action':action.action, 'time':action.time})
    ss=models.ScenarioStatus().query.filter_by(baby_id=baby.id).first()
    ss={'end_scenario':bool(ss.end_scenario), 'end_scenario_reason':str(ss.end_scenario_reason)}
    returnDict={
        'scenario_text':scenario_text,
        'PE':PE,
        'resusc':resusc,
        'history':history,
        'baby':babyDict,
        'warmer':warmer,
        'supplies':getSupplies(baby.id),
        'tasks': tasks,
        'PPIDict':ppb.getPPIDict(baby.id),
        'actionLog': actionLog,
        'scenario_status':ss
    }
    return returnDict

def updateWarmer(baby_id, warmer_dict):
    models.Warmer.query.filter_by(baby_id=baby_id).update(warmer_dict)
    db.session.commit()
    warmer=models.Warmer.query.filter_by(baby_id=baby_id).first()

def doTask(baby_id, taskName, time, **kwargs):
    ub=ppv_update.UpdateBaby(baby_id)
    ub.update(time, taskName=taskName, **kwargs)
    actionLog=models.Actionlog.query.filter_by(baby_id=baby_id).first()
    action="task:{name}, args:{kwargs}".format(name=taskName, kwargs=str(kwargs))
    a=models.Action(action=action, actionlog_id=actionLog.id, time=time)
    db.session.add(a)
    db.session.commit()
    app.logger.info(str(a.action)+" "+str(a.time))

