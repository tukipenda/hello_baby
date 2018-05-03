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
    models.create_baby(user, ppvScenario)

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
        'supplies':[]
    }
    return returnDict

def updateWarmer(user, warmer_dict):
