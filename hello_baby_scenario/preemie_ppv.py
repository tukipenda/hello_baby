import models
from models import db
import json
import preemie_ppv_data as data

baby_data=json.dumps(data.baby_data)
mom_data=json.dumps(data.mom_data)
baby_PE=json.dumps(data.PE)
supplies=json.dumps(data.supplyList)
warmer=json.dumps(data.warmer)
ppvScenario=models.Scenario(name="preemie_ppv", scenario=data.scenario, baby_data=baby_data, mom_data=mom_data, baby_PE=baby_PE, supplies=supplies, warmer=warmer)
db.session.add(ppvScenario)
db.session.commit()

def PPVCreateBaby(user):
    ppvScenario=models.Scenario.query.filter_by(name="preemie_ppv").first()
    return models.create_baby(user, ppvScenario)

def getSupplies(baby_id):
    supplies=models.Supply.query.filter_by(baby_id=baby_id)
    toReturn=[]
    for supply in supplies:
        s={}
        s['size']=supply.size
        s['name']=supply.name
        s['is_available']=supply.is_available
        s['is_using']=supply.is_using
        toReturn.append(s)
    return toReturn

def getSubDict(newdict, keys):
    return {key:newdict[key] for key in keys if (key in newdict.keys())}

def getScenarioData(user):
    scenario=models.Scenario.query.filter_by(name="preemie_ppv").first()
    baby=models.Baby.query.filter_by(user_id=user.id).first()
    babyDict=getSubDict(baby.__dict__, data.baby_data.keys())
    PE={}
    for e, m in models.PEDict.items():
        result=m.query.filter_by(baby_id=baby.id).first()
        PE[e]=getSubDict(result.__dict__, data.PE[e].keys())
    scenario_text=scenario.scenario
    mom=json.loads(scenario.mom_data)
    warmer=json.loads(scenario.warmer)
    returnDict={
        'scenario_text':scenario_text,
        'PE':PE,
        'mom':mom,
        'baby':babyDict,
        'warmer':warmer,
        'supplies':getSupplies(baby.id)
    }
    return returnDict

def updateWarmer(baby_id, warmer_dict):
    warmer_dict=json.loads(warmer_dict)
    warmer=models.Warmer.query.filter_by(baby_id=baby_id).update(warmer_dict)
    db.session.commit()

def doTask(baby_id, taskName, **kwargs):
    if taskName=="fetch":
        supply=models.Supply.query.filter_by(baby_id=baby_id, **kwargs).update(dict(is_available=True))
        db.session.commit()
    