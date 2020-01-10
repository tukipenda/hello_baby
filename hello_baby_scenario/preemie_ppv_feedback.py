#preemie_ppv feedback
import models
from models import db
from app import app
import json
import preemie_ppv_data as data
import preemie_ppv_update as ppv_update
from preemie_ppv_update import getSubDict, getSupplies
import pretty_print_baby as ppb

"""
Prior to delivery:
need to fetch pulse ox, 
ETT tubes
required settings for preemie

For good NRP need:
warm/dry/stimulate/suction infant <30 seconds
start PPV in under 60 seconds
do MRSOPA maneuvers
reassess heart/lungs
APGAR scores - need to request these

OK to have patient stay with mother?  Is CPAP sufficient?


"""
def printActionLog(baby_id):
    a=models.Actionlog().query.filter_by(baby_id=baby_id).first()
    app.logger.info(a)
    for l in a.actions:
        print(l.action)
        print(l.time)
    
    s=[[l.action, l.time] for l in a.actions]
    for k in s:
        if(("fetch" in k[0]) and ("pulse_ox" in k[0])):
            print(k[1])
            if k[1]<60:
                print("pass")
            else:
                print("fail")
        
# action requirements:
"""
[fetch pulse ox, 0]
[fetch ETT tube, 0]
etc... 

"""