#need create, teardown
#user, scenario,

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sqla
import sys
sys.path.append("/home/tukipenda/")
sys.path.append("/home/tukipenda/hello_baby/hello_baby_scenario")
import data
import json
from hello_baby import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Baby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    ga=db.Column(db.Text)
    neonatal_complications=db.Column(db.Text)

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
    temp=db.Column(db.Integer)
    weight=db.column(db.Float)

class PEResp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    breath_sounds=db.Column(db.Text)
    chest_rise=db.Column(db.Text)
    wob=db.Column(db.Text)
    is_grunting=db.Column(db.Boolean)
    is_spontaneous=db.Column(db.Boolean)

class PECardiac(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    murmur=db.Column(db.Text)
    femoral_pulse=db.Column(db.Text)
    brachial_pulse=db.Column(db.Text)

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
    positioning=db.Column(db.Text)
    is_airway_open=db.Column(db.Boolean)
    has_air_leak=db.Column(db.Boolean)

class CPR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    rate=db.Column(db.Integer)
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
    pip=db.Column(db.Integer)
    peep=db.Column(db.Integer)
    pop=db.Column(db.Integer)
    suction=db.Column(db.Integer)
    is_turned_on=db.Column(db.Boolean)
    temp_mode=db.Column(db.Text)
    fiO2=db.Column(db.Integer)
    flow=db.Column(db.Integer)

class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    circ_eff=db.Column(db.Float)
    volume_status=db.Column(db.Integer)
    card_health=db.Column(db.Integer)
    brain_health=db.Column(db.Integer)
    oxygenation=db.Column(db.Text) #oxygenation baby_data
    circulation=db.Column(db.Text)

class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'),
        nullable=False)
    supply_name=db.Column(db.Text)
    is_available=db.Column(db.Boolean)
    is_using=db.Column(db.Boolean)
    size=db.Column(db.Text, nullable=True)

class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario=db.Column(db.Text)
    baby_data=db.Column(db.Text)
    mom_data=db.Column(db.Text)
    baby_PE=db.Column(db.Text)


baby_data=json.dumps(data.baby_data)
mom_data=json.dumps(data.mom_data)
baby_PE=json.dumps(data.PE)
scenario=Scenario(scenario=data.scenario, baby_data=baby_data, mom_data=mom_data, baby_PE=baby_PE)

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

def createBaby(user, scenario):
    baby_data=json.loads(scenario.baby_data)
    baby_PE=json.loads(scenario.baby_PE)
    b=Baby(user_id=user.id, ga=baby_data['ga'], neonatal_complications=baby_data['neonatal_complications'])
    db.session.add(b)
    db.session.commit()
    baby_id=b.id
    for name,model in PEDict.items():
        subPE=model(baby_id=baby_id, **baby_PE[name])
        db.session.add(subPE)
        db.session.commit()

def getPEAttribute(baby_id, pe_name, attribute):
    model=PEDict[pe_name].query.filter_by(baby_id=baby_id).first()
    if (model and hasattr(model, attribute)):
        return getattr(model, attribute)
    else:
        return None

def setPEAttribute(baby_id, pe_name, attribute, value):
    model=PEDict[pe_name].query.filter_by(baby_id=baby_id).first()
    if (model and hasattr(model, attribute)):
        setattr(model, attribute, value)
        db.session.commit()
    else:
        pass
        #raise failure error
