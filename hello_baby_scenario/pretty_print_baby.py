from app import db, app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sqla
import json
from models import *

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