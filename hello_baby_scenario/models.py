from app import db, app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sqla
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    
# refactor_this - may not want scenario to be stored as a model, just as python code - that is probably the best thing actually.  
class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text) # needs to be unique
    scenario=db.Column(db.Text)
    baby_data=db.Column(db.Text)
    history=db.Column(db.Text)
    PE=db.Column(db.Text)
    warmer=db.Column(db.Text)
    supplies=db.Column(db.Text)
    tasks=db.Column(db.Text)
    vent=db.Column(db.Text)
    cpr=db.Column(db.Text)
    uvc=db.Column(db.Text)
    health=db.Column(db.Text)

class Baby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    ga=db.Column(db.Text)
    neonatal_complications=db.Column(db.Text)
    is_delivered=db.Column(db.Boolean)
    supplies = db.relationship('Supply', backref='baby', lazy=True)

    def __repr__(self):
        return '<Baby %r>' % self.ga

class PEVitals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    hr=db.Column(db.Integer)
    rr=db.Column(db.Integer)
    sbp=db.Column(db.Integer)
    dbp=db.Column(db.Integer)
    o2sat=db.Column(db.Integer)
    o2sat_updated=db.Column(db.Integer)
    temp=db.Column(db.Integer)
    weight=db.Column(db.Float)

class PEResp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    breath_sounds=db.Column(db.Text)
    chest_rise=db.Column(db.Text)
    wob=db.Column(db.Text)
    is_grunting=db.Column(db.Boolean)
    is_spontaneous=db.Column(db.Boolean)
    pneumo=db.Column(db.Text) #can be left, right, or none

class PECardiac(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    murmur=db.Column(db.Text)
    femoral_pulse=db.Column(db.Text)
    brachial_pulse=db.Column(db.Text)
    sounds=db.Column(db.Text)

class PEAbdomen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    bs=db.Column(db.Text)
    palpate=db.Column(db.Text)

class PESkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    color=db.Column(db.Text)
    is_dry=db.Column(db.Boolean)
    texture=db.Column(db.Text)

class PESecretions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    quantity=db.Column(db.Text)
    below_cords=db.Column(db.Boolean)
    color=db.Column(db.Text)
    thickness=db.Column(db.Text)

class PENeuro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    loc=db.Column(db.Text)
    motor_activity=db.Column(db.Text)
    motor_deficit=db.Column(db.Text)


class PEOther(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    scalp=db.Column(db.Text)
    clavicles=db.Column(db.Text)
    ears=db.Column(db.Text)
    eyes=db.Column(db.Text)
    umbilical_cord=db.Column(db.Text)
    palate=db.Column(db.Text)
    lips=db.Column(db.Text)
    gu=db.Column(db.Text)
    hips=db.Column(db.Text)
    spine=db.Column(db.Text)
    anus=db.Column(db.Text)

class Ventilation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    efficacy=db.Column(db.Float)
    is_mouth_open=db.Column(db.Boolean)
    positioning=db.Column(db.Integer)
    is_airway_open=db.Column(db.Boolean)
    has_air_leak=db.Column(db.Boolean)
    vent_type=db.Column(db.Text)
    set_rate=db.Column(db.Text)

class CPR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    event_rate=db.Column(db.Integer)
    btc_breaths=db.Column(db.Integer)
    btc_compressions=db.Column(db.Integer)
    cpr_depth=db.Column(db.Text)
    efficacy=db.Column(db.Float)


class UVC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    is_uvc_placed=db.Column(db.Boolean)
    medications_given=db.Column(db.Text)

class Warmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    is_turned_on=db.Column(db.Boolean)
    suction=db.Column(db.Integer)
    fio2=db.Column(db.Integer)
    flow=db.Column(db.Integer)
    pip=db.Column(db.Integer)
    peep=db.Column(db.Integer)
    pop=db.Column(db.Integer)
    temp_mode=db.Column(db.Text)

class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    circ_eff=db.Column(db.Float)
    volume_status=db.Column(db.Integer)
    card_health=db.Column(db.Integer)
    brain_health=db.Column(db.Integer)
    card_health_updated=db.Column(db.Integer)
    brain_health_updated=db.Column(db.Integer)
    oxygenation=db.Column(db.Text) #oxygenation baby_data
    circulation=db.Column(db.Text)

class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    name=db.Column(db.Text)
    is_available=db.Column(db.Boolean)
    is_using=db.Column(db.Boolean)
    use_simple=db.Column(db.Boolean) #can the supply be used with just a simple use action?
    size=db.Column(db.Text, nullable=True)
    pp=db.Column(db.Text)
    supply_type=db.Column(db.Text)

#needs to probably go in a different file
class Actionlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    actions = db.relationship('Action', backref='actionlog', lazy=True)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actionlog_id = db.Column(db.Integer, db.ForeignKey('actionlog.id'),
        nullable=False)
    action=db.Column(db.Text)
    time=db.Column(db.Float)

class ScenarioStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    end_scenario=db.Column(db.Boolean) #is the scenario over?
    end_scenario_reason=db.Column(db.Text) #why is the scenario over?

PEDict={
    'vitals':PEVitals,
    'resp':PEResp,
    'cardiac':PECardiac,
    'secretions':PESecretions,
    'abd':PEAbdomen,
    'neuro':PENeuro,
    'skin':PESkin,
    'other':PEOther
}

resuscDict={
    'vent':Ventilation,
    'cpr':CPR,
    'uvc':UVC,
    'health':Health
}

def create_baby(user, scenario):
    baby_data=json.loads(scenario.baby_data)
    PE=json.loads(scenario.PE)
    supplies=json.loads(scenario.supplies)
    warmer=json.loads(scenario.warmer)
    b=Baby(user_id=user.id, ga=baby_data['ga'], neonatal_complications=baby_data['neonatal_complications'])
    db.session.add(b)
    db.session.commit()
    baby_id=b.id
    for name,model in PEDict.items():
        subPE=model(baby_id=baby_id, **PE[name])
        db.session.add(subPE)
    db.session.commit()
    for key in ["vent", "cpr", "uvc", "health"]:
        kwargs=json.loads(getattr(scenario, key))
        for k,v in kwargs.items():
            if type(v)==list:
                kwargs[k]=json.dumps(v)
        resuscModel=resuscDict[key](baby_id=baby_id, **kwargs)
        db.session.add(resuscModel)
    
    for supply in supplies:
        newSupply=Supply(baby_id=baby_id, **supply)
        db.session.add(newSupply)
    db.session.commit()
    w=Warmer(baby_id=baby_id, **warmer)
    a=Actionlog(baby_id=baby_id)
    ss=ScenarioStatus(baby_id=baby_id, end_scenario=False, end_scenario_reason="")
    db.session.add(a)
    db.session.add(w)
    db.session.add(ss)
    db.session.commit()
    return b


db.create_all()

# plan - track last changes in JS, <15 seconds, will add <span> and then recreate PP PE dict here

def getPPInputFromDict(ed, rd, ga):
    PPIDict={} #pretty print input dictionary
    s=ed['skin']
    r=ed['resp']
    sec=ed['secretions']
    v=ed['vitals']
    c=ed['cardiac']
    abd=ed['abd']
    n=ed['neuro']
    o=ed['other']
    vent=rd['vent']

    #appearance
    dry="and dry" if s.is_dry else "and not dry"
    if r.chest_rise=="None":
        chest_rise="no chest rise"
    else:
        chest_rise=r.chest_rise
    grunting="Infant is grunting." if r.is_grunting else ""
    spontaneous="Infant is breathing spontaneously" if r.is_spontaneous else ""
    breathing=""
    vent_type=""
    if vent.vent_type=="intubated":
        vent_type="Infant is intubated."
    elif vent.vent_type=="ppv":
        vent_type="Infant is being bag-mask ventilated."
    else:
        breathing="Infant is breathing spontaneously."
        if v.rr==0:
            breathing="Infant is not breathing."
        elif v.rr<40:
            breathing="Infant is bradypneic and breathing spontaneously."
        elif v.rr>60:
            breathing="Infant is tachypneic and breathing spontaneously."
    wob=""
    if r.wob!="None":
        wob="Infant has "+r.wob+" work of breathing."
    if vent.is_mouth_open:
        mouth_open="open"
    else:
        mouth_open="closed"
    if vent.positioning==0:
        positioning="Infant is lying flat, no chin lift or jaw thrust"
    else: #vent.positioning should be 1
        positioning="Infant is in chin-lift position with jaw thrust"
    if vent.has_air_leak:
        air_leak="There is an air leak."
    else:
        air_leak="There is a good seal."
    PPIDict['appearance']={
        'ga':ga,
        'color':s.color,
        'dry':dry,
        'texture':s.texture.capitalize(),
        'breathing':breathing,
        'chest_rise':chest_rise,
        'grunting':grunting,
        'spontaneous':spontaneous,
        'vent_type':vent_type,
        'wob':wob,
        'mouth_open': mouth_open,
        'positioning':positioning
    }

    #respiratory
    breath_sounds="There are no breath sounds."
    if r.breath_sounds!="None":
        breath_sounds="Breath sounds are "+r.breath_sounds+"."
    
    air_leak=""
    if vent.vent_type=="ppv":
        if vent.has_air_leak:
            air_leak="There is an air leak."
        else:
            air_leak="There is a good seal."
        
    PPIDict['resp']={
        'breathing':breathing,
        'breath_sounds':breath_sounds,
        'chest_rise':chest_rise,
        'grunting':grunting,
        'spontaneous':spontaneous,
        'vent_type':vent_type,
        'wob':wob,
        'quantity':sec.quantity,
        'thickness':sec.thickness,
        'color':sec.color,
        'mouth_open': mouth_open,
        'positioning':positioning,
        'air_leak':air_leak
    }

    #cardiac
    PPIDict['cardiac']={
        'murmur':c.murmur,
        'b':c.brachial_pulse,
        'f':c.femoral_pulse,
        'hr':v.hr,
        'sounds':c.sounds.capitalize()
    }

    #abdomen
    PPIDict['abd']={
        'palpate':abd.palpate,
        'bs':abd.bs
    }
    
    #neuro
    cry="not crying"
    if not n.loc=="no cry":
        cry=n.loc
    moving=n.motor_activity
    PPIDict['neuro']={
        'cry':cry,
        'moving':moving
    }

    #other
    PPIDict['other']={
        'scalp':"does not have a caput" if (o.scalp=="no caput") else ("has a "+o.scalp),
    }
    for key in ['clavicles', 'ears','eyes', 'umbilical_cord', 'palate', 'lips', 'gu', 'hips', 'spine', 'anus']:
        PPIDict['other'][key]=getattr(o, key).capitalize()
    return PPIDict
    
# refactor_this
def getPrettyPrintPEFromDict(PPIDict):
    resultDict={}
    resultDict['appearance']="{ga} week old infant.  Skin is {color} {dry}. {texture}. {breathing} {vent_type} There is {chest_rise}. {wob} {grunting} Mouth is {mouth_open}. {positioning}.".format(**PPIDict['appearance']) 
    resultDict['resp']="{breathing} {breath_sounds} {vent_type} There is {chest_rise}. {wob} {grunting} Secretions are {quantity}, {thickness}, and {color}. ".format(**PPIDict['resp'])
    resultDict['cardiac']="{sounds}. There is {murmur}. Pulses are {b} brachial and {f} femoral.".format(**PPIDict['cardiac'])
    # removed HR from cardiac exam for now, as it appears as a separate test - Heart rate is {hr}.
    resultDict['abd']="Abdomen is {palpate}. {bs}.".format(**PPIDict['abd'])
    resultDict['neuro']="Infant is {cry}. Infant is {moving}.".format(**PPIDict['neuro'])
    resultDict['other']="Infant {scalp}. {clavicles}. Ears are {ears}. {eyes}. {umbilical_cord}. {palate}. {lips}. {gu}. {hips}. {spine}. {anus}".format(**PPIDict['other'])
    resultDict['vent']="{breathing} {vent_type} {air_leak} There is {chest_rise}. {wob} {grunting} Secretions are {quantity}, {thickness}, and {color}. Mouth is {mouth_open}. {positioning}.".format(**PPIDict['resp'])
    return resultDict

def getPPIDict(baby_id):
    ed={}
    rd={}
    for name,model in PEDict.items():
        ed[name]=model.query.filter_by(baby_id=baby_id).first()
    for name,model in resuscDict.items():
        rd[name]=model.query.filter_by(baby_id=baby_id).first()
    baby=Baby.query.filter_by(id=baby_id).first()
    return getPPInputFromDict(ed, rd, baby.ga)

def getHTMLValue(leaf, time):
    leaf['value']=str(leaf['value']) #cast to string to deal with numbers
    if(leaf['value'].strip()==""):
        return leaf['value']
    if (time-leaf['time'])<25000: #25 seconds
        return "<span class='updated'>{val}</span>".format(val=leaf['value'])
    else:
        return leaf['value']

def getHTMLPPIDict(PPIDict, time):
    if 'time' in PPIDict.keys():
        return getHTMLValue(PPIDict, time)
    else:
        return {k:getHTMLPPIDict(v, time) for k,v in PPIDict.items()}     
    
def getExams(PPIDict, time):
    PPIDict=getHTMLPPIDict(PPIDict, time)
    result_dict=getPrettyPrintPEFromDict(PPIDict)
    return result_dict