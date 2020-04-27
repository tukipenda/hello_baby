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

class ScenarioScoring:
    def __init__(self):
        self.results=""
        self.raw_result=""
        self.actions=""
                
    def scoreScenario(self, baby_id):
        self.actions=models.Actionlog().query.filter_by(baby_id=baby_id).first().actions
        self.raw_result=models.Results().query.filter_by(baby_id=baby_id).first()
        self.results=json.loads(self.raw_result.results)
   
        self.scorePE()
        self.scoreSupplies()
        self.scoreWarmerSetup()
        self.scoreBasic()
        self.scoreAirway()
        self.raw_result.results=json.dumps(self.results)
        db.session.commit()            

    def scoreSupplies(self):
        fetched_supplies=[]
        for action in self.actions:
            action_time=action.time
            ad=json.loads(action.action) #ad for action details
            if ad['task']=="fetch":
                if(action_time<30):
                    name=ad['args']['name']
                    if(ad['args']['size']):
                        name=name+"_"+ad['args']['size']
                    fetched_supplies.append(name)
        ETTS=["ett_2.5", "ett_3", "ett_3.5"]
        laryngoscopes=['laryngoscope_0', 'laryngoscope_1', 'laryngoscope_00']
        if(set(ETTS).issubset(set(fetched_supplies))):
            self.results['supplies_setup']['fetch_ETT']=1
        if(set(laryngoscopes).issubset(set(fetched_supplies))):
            self.results['supplies_setup']['fetch_laryngoscopes']=1
        items=['pulse_ox', 'hat', 'blankets', 'stethoscope', 'temp_probe']
        for item in items:
            if item in fetched_supplies:
                self.results['supplies_setup']["fetch_"+item]=1
    
    def supplyFetched(self, supplyName, supplyNumber):
        s=[[l.action, l.time] for l in self.actions]
        for k in s:
            if ("fetch"):
                pass
    
    #PEEP (5), PIP (20-25), POP, flow, FiO2 (21 >35 wks, 21-30 <35wks), suction set to correct values by 15s after start.  Heat turned on and set to manual before start
    #Values stay correct (except for PIP increasing after starting PPV)
    #could allow for brief drops of PIP or PEEP as long as it is corrected quickly, but maybe not to start
    def scoreWarmerSetup(self):
        pass

    #check HR (in first 30s, then how often?)
    #listen to heart (), listen to lungs (after PPV)
    #other exams by the end of this scenario
    def scorePE(self):
        for action in self.actions:
            action_time=action.time
            ad=json.loads(action.action) #ad for action details
            if ad['task']=="check_hr":
                if(action_time<30):
                    name=ad['args']['name']
                    if(ad['args']['size']):
                        name=name+"_"+ad['args']['size']
                    fetched_supplies.append(name)

    
    #first 30s, warm, dry, stim, hat, bulb suction, place temp probe, switch heat to baby mode (only after temp probe placed, and don't switch back)
    #timer started within 10s of delivery
    #pulse ox placed within 30s
    def scoreBasic(self):
        minTime=30
        actionsToScore=[
            ['dry', 'dry'],
            ['place_temp_probe', 'use_temp_probe'],
            ['stim', 'stimulate'],
            ['bulb_suction', 'bulb_suction'],
            ['place_hat', 'use_hat'],
        ]
        actionsToScore=[item+[minTime] for item in actionsToScore]
        actionsToScore.append(['place_pulse_ox', 'use_pulse_ox', 60])
        actionsToScore.append(['start_timer', 'start_timer', 10])
        for action in actionsToScore:
            self.results['base'][action[0]]=self.actionCompletedByTime(action[1], action[2])

        # now need to add heat baby mode

    #start PPV within 60s.  Correct rate set. Check HR and lungs after starting PPV.  How much of MRSOPA is required?
    def scoreAirway(self):
        pass
   

    #method to check if action has been done by certain time.  
    def actionCompletedByTime(self, action_name, time):
        for action in self.actions:
            action_time=action.time
            if action_time<time:
                ad=json.loads(action.action)
                if(ad['task']==action_name):
                    return True
        return False
    
    #method to check if action has been done after first time another action has done (within a certain time frame)
    def actionCompletedAfterAction(self, action_name, prior_action, time_elapsed):
        first_action_time="blank"
        for action in self.actions:
            ad=json.loads(action.action)
            if(ad['task']==prior_action):
                if(first_action_time=="blank"):
                    first_action_time=action.time
                else:
                    if(first_action_time>action.time):
                        first_action_time=action.time
        if(first_action_time!="blank"):
            for action in self.actions:
                action_time=action.time                
                ad=json.loads(action.action)                
                if(ad['task']==action_name):
                    if action_time<(time+time_elapsed):
                            return True
        else:
            return False