import models
from models import db
import json
import preemie_ppv_data as data
import uuid

baby_data=json.dumps(data.baby_data)
mom_data=json.dumps(data.mom_data)
baby_PE=json.dumps(data.PE)
supplies=json.dumps(data.supplyList)
ppvScenario=models.Scenario(name="preemie_ppv", scenario=data.scenario, baby_data=baby_data, mom_data=mom_data, baby_PE=baby_PE, supplies=supplies)
db.session.add(ppvScenario)
db.session.commit()
PPVCreateBaby=lambda x: models.create_baby(x, ppvScenario)

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
    returnDict={
        'scenario_text':scenario_text,
        'PE':PE,
        'mom':mom,
        'baby':babyDict
    }
    return returnDict