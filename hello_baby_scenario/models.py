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

    
#to_remove - may not want scenario to be stored as a model, just as python code - that is probably the best thing actually.  
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
    results=db.Column(db.Text)

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
   

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    results=db.Column(db.Text)
    
    
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
    r=Results(baby_id=baby_id, results=scenario.results)
    db.session.add(a)
    db.session.add(w)
    db.session.add(ss)
    db.session.add(r)
    db.session.commit()
    return b


db.create_all()

# plan - track last changes in JS, <15 seconds, will add <span> and then recreate PP PE dict here