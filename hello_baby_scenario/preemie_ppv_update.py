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

#tasks below still require db session commit
def fetchSupply(baby_id, **kwargs):
    models.Supply.query.filter_by(baby_id=baby_id, **kwargs).update(dict(is_available=True))

def useSupply(baby_id, **kwargs):
    supply=models.Supply.query.filter_by(baby_id=baby_id, **kwargs).first()
    if(supply.is_available):
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

taskDict={
    "fetch":fetchSupply,
    "use":useSupply,
    "dry":dry,
    "stimulate":stimulate,
    "deliver_baby":deliver_baby
}

#this is hacky - need to fix this
class UpdateBaby:
    def __init__(self, baby_id):
        self.baby_id=baby_id
        self.PE={}
        for e, m in models.PEDict.items():
            result=m.query.filter_by(baby_id=self.baby_id).first()
            self.PE[e]=getSubDict(result.__dict__, data.PE[e].keys())
        self.warmer=models.Warmer.query.filter_by(baby_id=self.baby_id).first()
        self.supplies=getSupplies(self.baby_id)
        self.time=0
        self.db=db

    def getSupply(self, name, size=None):
        for supply in self.supplies:
            if((supply['name']==name) and (not supply['size'] or (supply['size']==size))):
                return supply
        return None

    def update(self, time):#taskName, **kwargs):
        self.time=time
        self.updateVitals(time)
        for e, m in models.PEDict.items():
            result=m.query.filter_by(baby_id=self.baby_id)
            result.update(self.PE[e])
        self.db.session.commit()

    def updateVent(self):
        pass

    def updateUVC(self):
        pass

    def updateCPR(self):
        pass

    def updateHealth(self):
        pass

    def updatePE(self):
        pass

    def updateVitals(self, time):
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
                        temp=round(temp+0.05, 2)
                    if (self.warmer.temp_mode=="baby" and temp>37):
                        temp=round(temp-0.05, 2)
                else:
                    if temp>34:
                        temp=round(temp-0.05, 2)
            self.PE['vitals']['temp']=temp




        def updateO2sat():
            pass

        updateHR()
        updateRR()
        updateTemp()