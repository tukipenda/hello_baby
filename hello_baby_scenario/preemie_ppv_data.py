from app import app
scenario="You are called by the OB team for a preterm delivery by SVD. The baby's gestational age is estimated at 32 weeks.  Mom is 37 years old, afebrile, and prenatal labs are normal."
baby_data={"ga":"32", "neonatal_complications":"None", "delivery":"SVD", "is_delivered":False}

history="Mom is a 37 year old G2P1 woman.  Baby is EGA 32 weeks, delivery by SVD.  She is VZVI, RI, HIV-, Hep B negative, RPRNR, GC/Chlamydia negative, and GBS negative.  \
She has been afebrile.  Rupture of membranes occurred 36 hours ago with clear fluids.  She received one dose of betamethasone 24 hours ago."

warmer={
    "is_turned_on":False,
    "suction":0,
    "fio2":100,
    "flow":0,
    "temp_mode":"manual",
    "peep":0,
    "pip":0,
    "pop":0
}

#Need to change the exams so they are less text-based.
#I deleted APGAR for now,not including malformations, BP, EKG, or 4-extremity sats
vitals={'o2sat':55, 'o2sat_updated':0, 'hr':120, 'rr':0, 'sbp':75, 'dbp':50, 'temp':35.2, 'weight':2.25}
resp={"breath_sounds":"None", "chest_rise":"None", "wob":"None", "is_grunting":False, "is_spontaneous":False}
cardiac={"murmur":"no murmur", "sounds": "normal S1/S2", "femoral_pulse":"2+", "brachial_pulse":"2+"}
abd={"bs":"+bs", "palpate":"soft, no HSM"}
skin={"color":'blue', "is_dry":False, "texture":"term infant skin"}
secretions={"quantity":'moderate', "below_cords":False, "color":'clear', "thickness":'thin'}
neuro={"loc":'no cry', "motor_activity":"not moving", "motor_deficit":"none"}
other={"scalp":'no caput', "clavicles":'no clavicular fracture', "ears":'normally positioned',
             "eyes":'red reflex intact bilaterally', "umbilical_cord":"normal 3 vessel cord", "palate":'palate intact', "lips":'no cleft lips', "gu":'normal genitalia',
             "hips":'no hip click', "spine":'no dimple', "anus":'patent anus'}

PE={"vitals":vitals, "resp":resp, "cardiac":cardiac, "abd":abd, "skin":skin, "secretions":secretions, "neuro":neuro, "other":other}

vent={
    'efficacy':0,
    'is_mouth_open':False,
    'positioning': 0, #alternative is 1
    'is_airway_open': True,
    'has_air_leak': False,
    'set_rate':0,
    'vent_type': "spontaneous" #options include ppv, intubated
}

cpr={
    'event_rate':0, #ideal is 120
    'btc_breaths':0, #ideal is 1:3
    'btc_compressions':0, #ideal is 3
    'cpr_depth':"0", #ideal is 1/3
    'efficacy':0
}

uvc={
    'is_uvc_placed':False,
    'medications_given':[]
}

health={
    'circ_eff':1.0,
    'volume_status':3,
    'card_health':4, #4 is great, 3 is HR<100 but >60 (mild injury), 2 is HR<60 (significant injury), 1 is pulseless but heart can recover, 0 is death
    'brain_health':4, #4 is good, 3 is risk of injury (that will recover with some oxygen), 2 is mild injury (that will improve with oxygen), 1 is severe injury (that will show minimal improvement with oxygen), 0 is death
    'card_health_updated':0, #time of last update
    'brain_health_updated':0, #time of last update
    'oxygenation':[],
    'circulation':[]
}

resusc={
    'vent':vent,
    'cpr':cpr,
    'uvc':uvc,
    'health':health
}

basic_supplies=[
            "hat",
            "blankets",
            "bulb_suction",
            "cord_clamp"
        ]
resp_supplies=[
    "meconium_aspirator",
    "stethoscope"
]
warming_supplies=[
    "transwarmer",
    "plastic_bag"
]
monitor_supplies=[
    "pulse_ox",
    "temp_probe"
]
proc_supplies=[
    "scalpel",
    "flush",
    "UVC"
]
med_supplies=[
    "epinephrine",
    "normal_saline_bag"
]
supplies=[]

#basic supplies
for (supplyList,supply_type) in [(basic_supplies, 'basic'), (resp_supplies, 'resp'), (warming_supplies, 'warming'), (monitor_supplies, 'monitors'), (proc_supplies, 'procedures'), (med_supplies, 'meds')]:
    for supply in supplyList:
        supplies.append({"name":supply, "size":None, 'supply_type':supply_type})

#laryngoscopes
supplies.extend([{"name":'laryngoscope', "size":size, 'supply_type':'resp'} for size in ["0", "1", "00"]])

#ETTs
supplies.extend([{"name":'ett', "size":size, 'supply_type':'resp'} for size in ["2.5", "3", "3.5"]])

#masks
supplies.extend([{"name":'mask', "size":size, 'supply_type':'basic'} for size in ["Infant", "Preemie"]])


#need to make pp actually pp
def setSupplyParams(supply):
    if supply['name']=='mask':
        supply['is_available']=True
    else:
        supply['is_available']=False
    supply["is_using"]=False
    if supply['size']:
        supply["pp"]=supply['name']+": "+supply['size']
    else:
        supply['pp']=" ".join(supply['name'].split("_")).title()
        
    #set whether supply is being used
    if supply['name'] in (basic_supplies+monitor_supplies+warming_supplies):
        supply['use_simple']=True
    else:
        supply['use_simple']=False
    return supply

#list comprehension to modify list of supplies
supplies=[setSupplyParams(supply) for supply in supplies]

#fetch tasks
tasks=[{
        'name':'fetch_'+supply['name'],
        'supply_name':supply['name'],
        'size':supply['size'],
        'pp':'fetch '+supply['pp'],
        'type':'fetch',
    } for supply in supplies]

#use tasks
tasks.extend([{
        'name':'use_'+supply['name'],
        'supply_name':supply['name'],
        'size':supply['size'],
        'in_progress':'Using '+supply['pp'],
        'pp':'Use '+supply['pp'],
        'type':'simple',
    } for supply in supplies if supply['use_simple']])

#simple tasks
simpleTasks=[
    {
       'name':'dry',
        'pp':'Dry',
        'in_progress':"Drying",
        'requires':['blankets'],
        'type':'simple'
    },
    {
       'name':'stimulate',
        'pp':'Stimulate Baby',
        'in_progress':"Stimulating Baby",
        'type':'simple'
    },
    {
       'name':'bulb_suction',
        'pp':'Bulb Suction',
        'in_progress':"Suctioning with bulb",
        'requires':['bulb_suction'],
        'type':'simple'
    },
    {
       'name':'deep_suction',
        'pp':'Deep Suction',
        'in_progress':"Suctioning",
        'type':'simple'
    }
]

respTasks=[
    {
       'name':'adjust_mask',
        'pp':'Adjust Mask',
        'in_progress':"Adjusting Mask",
        'type':'resp'
    },
    {
       'name':'reposition',
        'pp':'Reposition',
        'in_progress':"Repositioning",
        'type':'resp'
    },
    {
       'name':'open_mouth',
        'pp':'Open Mouth',
        'in_progress':"Opening Mouth",
        'type':'resp'
    }
]

ventTasks=[
    {
       'name':'start_ppv',
        'pp':'start_ppv',
        'in_progress':"Starting PPV",
        'type':'vent'
    },
    {
       'name':'stop_ppv',
        'pp':'stop_ppv',
        'in_progress':"Stopping PPV",
        'type':'vent'
    },
    {
       'name':'intubate',
        'pp':'Intubate',
        'in_progress':"Intubating",
        'type':'vent'
    },
    {
       'name':'extubate',
        'pp':'Extubate',
        'in_progress':"Extubating",
        'type':'vent'
    }
]

tasks.extend(simpleTasks)
tasks.extend(respTasks)
tasks.extend(ventTasks)