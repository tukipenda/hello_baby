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


requirements:
required supplies -> make sure you fetch all of them
"fetch" "pulse_ox" by delivery
"fetch" "hat" by delivery
"fetch" "ETT size 0" by delivery etc...
settings for warmer
"warm", "dry", "stimulate", "suction" by 30 seconds
place hat by 30 seconds
check HR by 30 seconds
listen to heart and lung sounds by ***time
place pulse ox by ***
place temp probe by ***
"start PPV" by 60 seconds
MRSOPA steps

Good Feedback: (color code green vs. red)
Fetch - you correctly fetched the following items before delivery
Negative feedback:
You fetched this item, but after delivery
You did not fetch the following items

You correctly set the warmer to the following settings
You did not correctly set ***

action, time of action, (performed on time, not performed, performed late), feedback about action

one of the confusing things is what should the UI be like.  Designing a good UI is probably the key to making this effective.  
"""

def score(results):
    score={}
    for k,v in results.items():
        vs=results[k].values()
        score[k]=round(100*float(sum(vs))/len(vs))
    score['overall']=round(0.2*sum(score.values()))
    return(score)

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
            if k[1]<30:
                print("pass")
            else:
                print("fail")

def scoreScenario(baby_id):
    a=models.Actionlog().query.filter_by(baby_id=baby_id).first()
    app.logger.info(a)
    for l in a.actions:
        print(l.action)
        print(l.time)
    
    s=[[l.action, l.time] for l in a.actions]
    for k in s:
        if(("fetch" in k[0]) and ("pulse_ox" in k[0])):
            print(k[1])
            if k[1]<30:
                print("pass")
            else:
                print("fail")
    
#check if pulse ox was fetched

            
# action requirements:
"""
[fetch pulse ox, 0]
[fetch ETT tube, 0]
etc... 

"""