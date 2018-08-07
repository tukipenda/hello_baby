import models
from models import db
from app import app
import preemie_ppv_data as data
import json
import numpy as np

def getSubDict(newdict, keys):
    return {key:newdict[key] for key in keys if (key in newdict.keys())}

def getSupplies(baby_id):
    supplies=models.Supply.query.filter_by(baby_id=baby_id)
    return [{name:getattr(supply, name) for name in 
             ['size', 'name', 'is_available', 'is_using', 'use_simple', 'pp', 'supply_type']}
            for supply in supplies]

def getSupply(baby_id, name, size=None):
    supplies=getSupplies(baby_id)
    for supply in supplies:
        if((supply['name']==name) and (not supply['size'] or (supply['size']==size))):
            return supply
    return None

#tasks below still require db session commit
def updatewarmer(baby_id, **kwargs):
    models.Warmer.query.filter_by(baby_id=baby_id).update(kwargs)

def fetchSupply(baby_id, **kwargs):
    models.Supply.query.filter_by(baby_id=baby_id, **kwargs).update(dict(is_available=True))

def useSupply(baby_id, **kwargs):
    name=kwargs['name']
    supply=models.Supply.query.filter_by(baby_id=baby_id, **kwargs).first()
    if(supply.is_available):
        models.Supply.query.filter_by(baby_id=baby_id, name=name).update(dict(is_using=False)) #remove other supplies already being used
        supply.is_using=True
    else:
        pass #error supply is not available

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

taskDict={
    "fetch":fetchSupply,
    "use":useSupply,
    "dry":dry,
    "stimulate":stimulate,
    "deliver_baby":deliver_baby,
    "start_ppv":start_ppv,
    'stop_ppv':stop_ppv,
    'set_rate':set_rate,
    'updatewarmer':updatewarmer
}

# refactor_this
#this is hacky - need to fix this - also needs major testing!!!
class UpdateBaby:
    def __init__(self, baby_id):
        self.baby_id=baby_id
        self.PE={}
        self.resusc={}
        self.taskName=None
        self.time=0 #remember time is in ms
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
        for e, m in models.resuscDict.items():
            result=m.query.filter_by(baby_id=self.baby_id)
            result.update(self.resusc[e])
        self.db.session.commit()

    def taskUpdate(self, time, taskName, **kwargs):
        self.taskName=taskName
        if taskName in taskDict:
            taskDict[taskName](self.baby_id, **kwargs)
        self.db.session.commit()
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
        for e, m in models.resuscDict.items():
            result=m.query.filter_by(baby_id=self.baby_id)
            result.update(self.resusc[e])
        self.db.session.commit()

    def updateVent(self):
        if self.resusc['vent']['vent_type'] in ['ppv', 'intubated']:
            self.PE['vitals']['rr']=self.resusc['vent']['set_rate']

        if self.taskName=="adjustMask":
            self.resusc['vent']['has_air_leak']=False


        if self.taskName=="reposition":
            self.resusc['vent']['positioning']=1

        if self.taskName=="open_mouth":
            self.resusc['vent']['is_mouth_open']=True

        if self.taskName=="deep_suction":
            self.PE['secretions']['quantity']='minimal'

        v=self.resusc['vent']
        r=self.PE['resp']
        if((not v['has_air_leak']) and (v['is_mouth_open'])):
            v['efficacy']=0.4
            r['chest_rise']='poor chest rise'
            if v['positioning']==1:
                v['efficacy']=0.8
                r['breath_sounds']="breath sounds present bilaterally, difficult to hear"
                r['chest_rise']="good chest rise"
                if(self.PE['secretions']['quantity'])=='minimal':
                    v['efficacy']=1
                    r['breath_sounds']="clear breath sounds bilaterally"

    def updateUVC(self):
        pass

    def updateCPR(self):
        pass

    def get_last_od(self, seconds):
        oxygenation=json.loads(self.resusc['health']['oxygenation'])
        circulation=json.loads(self.resusc['health']['circulation'])
        oxygen_delivery=[a*b for a,b in zip(oxygenation,circulation)]
        count=int(seconds/5)
        last=oxygen_delivery[-count:]
        last=sum(last)/float(len(last)) if len(last)!=0 else 0
        return last

    #maybe I can start to include some formulas - like the O2 delivery formula at some point
    def updateHealth(self): #this is going to need some serious testing!!!

        oxygenation=json.loads(self.resusc['health']['oxygenation'])
        ndelta=len(oxygenation)
        tdelta=self.time//5000
        if tdelta>ndelta:
            for x in range(tdelta-ndelta):
                oxygenation.append(self.resusc['vent']['efficacy'])
        self.resusc['health']['oxygenation']=json.dumps(oxygenation)

        #update circ_eff - this needs some editing to account for other things like CPR, etc...
        card_health=self.resusc['health']['card_health']
        if card_health==4:
            circ_eff=1.0
        elif card_health==3:
            circ_eff=0.75
        elif card_health==2:
            circ_eff=0.25
        else:
            circ_eff=0
        self.resusc['health']['circ_eff']=circ_eff

        #update circulation
        circulation=json.loads(self.resusc['health']['circulation'])
        ndelta=len(circulation)
        tdelta=self.time//5000
        if tdelta>ndelta:
            for x in range(tdelta-ndelta):
                circulation.append(circ_eff)
        self.resusc['health']['circulation']=json.dumps(circulation)

        ctime=self.resusc['health']['card_health_updated']
        btime=self.resusc['health']['brain_health_updated']

        #currently this function does not account for the time being less than 30 or 60 seconds
        def get_card_health(card_health):
            if self.get_last_od(60)<0.2:
                if (card_health>0) and (self.time-ctime)>60000:
                    card_health=card_health-1
                    self.resusc['health']['card_health_updated']=self.time
                elif (card_health<4) and (self.time-ctime)>60000:
                    card_health=card_health+1
                    self.resusc['health']['card_health_updated']=self.time
            return card_health

        self.resusc['health']['card_health']=get_card_health(self.resusc['health']['card_health'])

        # now we need to update brain health
        def get_brain_health(brain_health):
            if ((brain_health==4) and (self.get_last_od(120)<0.2) and (self.time-btime))>120000:
                brain_health=brain_health-1
            elif self.get_last_od(60)<0.2:
                if (brain_health>0) and (self.time-btime)>60000:
                    brain_health=brain_health-1
                    self.resusc['health']['brain_health_updated']=self.time
                elif (brain_health<4) and (brain_health>1) and (self.time-btime)>60000:
                    brain_health=brain_health+1
                    self.resusc['health']['brain_health_updated']=self.time
            return brain_health

        self.resusc['health']['brain_health']=get_brain_health(self.resusc['health']['brain_health'])

    def updatePE(self):

        def updateResp():
            pass

        def updateCardiac():
            if self.resusc['health']['card_health']<2:
                self.PE['cardiac']['sounds']="no heart sounds audible"
                self.PE['cardiac']['femoral_pulse']="absent"
                self.PE['cardiac']['brachial_pulse']="absent"
            if self.resusc['health']['card_health']==2:
                self.PE['cardiac']['sounds']="normal S1/S2"
                self.PE['cardiac']['femoral_pulse']="1+"
                self.PE['cardiac']['brachial_pulse']="1+"
            if self.resusc['health']['card_health']>2:
                self.PE['cardiac']['sounds']="normal S1/S2"
                self.PE['cardiac']['femoral_pulse']="2+"
                self.PE['cardiac']['brachial_pulse']="2+"

        def updateSecretions():
            pass

        def updateNeuro():
            pass

        updateResp()
        updateCardiac()
        updateSecretions()
        updateNeuro()

    def updateVitals(self):
        def updateHR():
            if (not self.taskName): #I don't want to update HR for a task update, just q5s.
                hr=self.PE['vitals']['hr']
                card_health=self.resusc['health']['card_health']
                ox_eff=self.resusc['vent']['efficacy']
                if card_health in [0, 1]:
                    hr=0
                sign=0
                if ox_eff>0.8:
                    sign=1
                elif ox_eff<0.5:
                    sign=-1
                if card_health==2:
                    if (hr>40) or (sign==1):
                        hr=hr+np.random.normal(sign*5, 4)
                    elif hr>30:
                        hr=hr+np.random.normal(0, 2)
                    else:
                        hr=hr+np.random.normal(5, 4)
                if card_health==3:
                    if hr>100:
                        hr=hr-np.random.normal(5, 4)
                    elif hr>70:
                        hr=hr+np.random.normal(sign*5, 4)
                    elif (hr>60) and (sign!=1):
                        hr=hr+np.random.normal(0, 4)
                    else:
                        hr=hr+np.random.normal(2, 4)
                if card_health==4:
                    if (hr>140) and (sign==1):
                        hr=hr+np.random.normal(0, 3)
                    elif hr>90:
                        hr=hr+np.random.normal(sign*5, 4)
                    else:
                        hr=hr+np.random.normal(5, 4)
                hr=int(hr)
                self.PE['vitals']['hr']=hr


        def updateRR():
            if not self.taskName: #updating when not a specific task (will need another for extubation/stopping PPV)
                card_health=self.resusc['health']['card_health']
                rr=self.PE['vitals']['rr']
                if self.resusc['vent']['vent_type']=='spontaneous':
                    if self.get_last_od(45)>0.8:
                        if card_health==4:
                            if rr==0:
                                rr=40
                            else:
                                rr=rr+np.random.normal(0, 3)
                        if card_health==3:
                            if rr==0:
                                rr=30
                            else:
                                rr=rr+np.random.normal(0, 3)
                    elif rr!=0:
                        rr=rr-np.random.normal(4, 4)
                    self.PE['vitals']['rr']=int(rr)
                else:
                    self.PE['vitals']['rr']=self.resusc['vent']['set_rate']

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
            if (not self.taskName):
                app.logger.info(self.get_last_od(30))
                app.logger.info(self.time)
                o2sat=self.PE['vitals']['o2sat']
                otime=self.PE['vitals']['o2sat_updated']
                app.logger.info(o2sat)
                if o2sat>95:
                    o2sat=o2sat+np.random.normal(0, 2)                
                    self.PE['vitals']['o2sat']=round(o2sat, 2)
                    return
                if (self.time-otime)>30000:
                    self.PE['vitals']['o2sat_updated']=self.time
                    if self.get_last_od(30)>0.8:
                        o2sat=o2sat+5+np.random.normal(0, 2)

                    if self.get_last_od(30)<0.2:
                        o2sat=o2sat-5-np.random.normal(0, 2)
                    else:
                        o2sat=o2sat+np.random.normal(0, 2)
                else:
                    if self.get_last_od(30)>0.8:
                        o2sat=o2sat+0.5+np.random.normal(0, 0.5)
                    if self.get_last_od(30)<0.2:
                        o2sat=o2sat-0.5-np.random.normal(0, 0.5)
                    else:
                        o2sat=o2sat+np.random.normal(0, 0.5)
                if o2sat>100:
                    o2sat=100
                if o2sat<0:
                    o2sat=0
                self.PE['vitals']['o2sat']=round(o2sat, 2)


        updateHR()
        updateRR()
        updateTemp()
        updateO2sat()