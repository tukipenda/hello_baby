import models
from models import db
from app import app
import preemie_ppv_data as data
import json

def getSubDict(newdict, keys):
    return {key:newdict[key] for key in keys if (key in newdict.keys())}

def getSupplies(baby_id):
    supplies=models.Supply.query.filter_by(baby_id=baby_id)
    toReturn=[]
    for supply in supplies:
        s={}
        s['size']=supply.size
        s['name']=supply.name
        s['is_available']=supply.is_available
        s['is_using']=supply.is_using
        s['pp']=supply.pp
        toReturn.append(s)
    return toReturn

def getSupply(baby_id, name, size=None):
    supplies=getSupplies(baby_id)
    for supply in supplies:
        if((supply['name']==name) and (not supply['size'] or (supply['size']==size))):
            return supply
    return None

#tasks below still require db session commit
def fetchSupply(baby_id, **kwargs):
    models.Supply.query.filter_by(baby_id=baby_id, **kwargs).update(dict(is_available=True))

def useSupply(baby_id, **kwargs):
    name=kwargs['name']
    supply=models.Supply.query.filter_by(baby_id=baby_id, **kwargs).first()
    if(supply.is_available):
        models.Supply.query.filter_by(baby_id=baby_id, name=name).update(dict(is_using=False)) #remove other supplies already being used
        supply.is_using=True

def dry(baby_id):
    skin=models.PESkin.query.filter_by(baby_id=baby_id).first()
    skin.is_dry=True
    db.session.commit()
    test=models.PESkin.query.filter_by(baby_id=baby_id).first()
    
def stimulate(baby_id):
    pass

def deliver_baby(baby_id):
    baby=models.Baby.query.filter_by(id=baby_id).update(dict(is_delivered=True))


def start_ppv(baby_id):
    vent=models.Ventilation.query.filter_by(baby_id=baby_id).first()
    vent.vent_type="ppv"
    db.session.commit()

def stop_ppv(baby_id):
    vent=models.Ventilation.query.filter_by(baby_id=baby_id).first()
    vent.vent_type="spontaneous"
    db.session.commit()

def set_rate(baby_id, set_rate):
    vent=models.Ventilation.query.filter_by(baby_id=baby_id).first()
    vent.set_rate=set_rate
    db.session.commit()
    app.logger.info(vent)
    
taskDict={
    "fetch":fetchSupply,
    "use":useSupply,
    "dry":dry,
    "stimulate":stimulate,
    "deliver_baby":deliver_baby,
    "startPPV":start_ppv,
    'stopPPV':stop_ppv,
    'set_rate':set_rate
}

#this is hacky - need to fix this
class UpdateBaby:
    def __init__(self, baby_id):
        self.baby_id=baby_id
        self.PE={}
        self.resusc={}
        self.taskName=None
        self.time=0
        self.db=db
    
    def getData(self):
        for e, m in models.PEDict.items():
            result=m.query.filter_by(baby_id=self.baby_id).first()
            self.PE[e]=getSubDict(result.__dict__, data.PE[e].keys())
        for e, m in models.resuscDict.items():
            result=m.query.filter_by(baby_id=self.baby_id).first()
            self.resusc[e]=getSubDict(result.__dict__, data.resusc[e].keys())
        self.warmer=models.Warmer.query.filter_by(baby_id=self.baby_id).first()
        self.supplies=getSupplies(self.baby_id)

    def getSupply(self, name, size=None):
        for supply in self.supplies:
            if((supply['name']==name) and (not supply['size'] or (supply['size']==size))):
                return supply
        return None

    def update(self, time, **kwargs):#taskName, **kwargs):
        self.getData()
        self.time=time
        self.updateVent()
        self.updateUVC()
        self.updateCPR()
        self.updateHealth()
        self.updatePE()
        self.updateVitals()
        for e, m in models.PEDict.items():
            result=m.query.filter_by(baby_id=self.baby_id)
            result.update(self.PE[e])
        self.db.session.commit()
    
    def taskUpdate(self, time, taskName, **kwargs):
        self.taskName=taskName
        if taskName in taskDict:
            taskDict[taskName](self.baby_id, **kwargs)
        self.db.session.commit()
        self.getData()
        app.logger.info(self.resusc['vent'])
        self.update(time, **kwargs)

    def updateVent(self):      
        if self.resusc['vent']['vent_type'] in ['ppv', 'intubated']:
            self.PE['vitals']['rr']=self.resusc['vent']['set_rate']

    def updateUVC(self):
        pass

    def updateCPR(self):
        pass

    def updateHealth(self):
        pass

    def updatePE(self):
        pass

    def updateVitals(self):
        def updateHR():
            pass

        def updateRR():
            pass

        def updateTemp():
            temp=self.PE['vitals']['temp']
            #if warmer not on, lose 0.05 C every 5 seconds until temp is 33
            #if warmer on and hat on, baby dry, GA high enough, gain 0.1 C every 5 seconds until temp is 37 (if baby mode is on)
            #if baby mode is off, temp keeps increasing to 39
            # if hat not on, baby not dry - temp stays at 35
            if not self.warmer.is_turned_on:
                if temp>33:
                    temp=round(temp-0.05, 2)
            else:
                if ((self.PE['skin']['is_dry']) and (self.getSupply("hat")['is_using']==True)):
                    if (self.warmer.temp_mode=="manual" or temp<37):
                        if(temp<39):
                            temp=round(temp+0.05, 2)
                    if (self.warmer.temp_mode=="baby" and temp>37):
                        temp=round(temp-0.05, 2)
                else:
                    if temp>34:
                        temp=round(temp-0.05, 2)
                        
                    else:
                        temp=round(temp+0.05, 2)
            self.PE['vitals']['temp']=temp




        def updateO2sat():
            pass

        updateHR()
        updateRR()
        updateTemp()