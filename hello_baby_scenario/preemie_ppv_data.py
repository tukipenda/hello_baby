scenario="You are called by the OB team for a stat C/S. Mom is 25 years old, and gestational age is 32 weeks."
baby_data={"ga":"32", "neonatal_complications":"None", "delivery":"C/S", "is_delivered":False}

mom_data={"age":25,
  "PNL":"Prenatal labs: VZVI, RI, HIV negative, Hep B negative, RPRNR, GC/Chlamydia negative",
"hsv":"No history of HSV and has no active lesions.",
  "gbs":"GBS+.  She was febrile to 38.1, and received ampicillin 2 hours before delivery.",
  "rom":"ROM occurred 16 hours ago.",
  "gp":"G1PO"}

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
vitals={'o2sat':55, 'hr':120, 'rr':0, 'sbp':75, 'dbp':50, 'temp':35, 'weight':2.25}
resp={"breath_sounds":"None", "chest_rise":"None", "wob":"None", "is_grunting":False, "is_spontaneous":False}
cardiac={"murmur":"no murmur", "femoral_pulse":"2+", "brachial_pulse":"2+"}
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
    'positioning': "lying flat, no chin lift or jaw thrust",
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
    'brain_health':3, #3 is good, 2 is minor injury, 1 is severe injury, 0 is death
    'oxygenation':[],
    'circulation':[]
}

resusc={
    'vent':vent,
    'cpr':cpr,
    'uvc':uvc,
    'health':health
}

simple_supplies=[
            "pulse_ox",
            "hat",
            "transwarmer",
            "plastic_bag",
            "temp_probe",
            "blankets",
            "bulb_suction",
            "meconium_aspirator",
            "stethoscope",
            "epinephrine",
            "normal_saline_bag",
            "cord_clamp",
            "scalpel",
            "flush",
            "UVC"
        ]
supplyList=[]
for supply in simple_supplies:
    supplyList.append({"name":supply, "size":None})

for size in ["0", "1", "00"]:
    supplyList.append({"name":'laryngoscope', "size":size})

for size in ["2.5", "3", "3.5"]:
    supplyList.append({"name":'ett', "size":size})

for supply in supplyList:
    supply["is_available"]=False
    supply["is_using"]=False
    supply['pp']=supply['name']
    if supply['size']:
        supply["pp"]=supply['name']+": "+supply['size']

for size in ["Infant", "Preemie"]:
    supplyList.append({"name":'mask', "size":size, "is_available":True, "is_using":False, 'pp': ('mask: '+size)})


availableSupplies=[
            "temp_probe",
            "blankets",
            "meconium_aspirator",
            "stethoscope",
            "cord_clamp",
]

for supply in supplyList:
    if supply['name'] in availableSupplies:
        supply['is_available']=True
    if supply['name']=="ett":
        if supply['size'] in ["3", "3.5"]:
            supply['is_available']=True
    if supply['name']=='laryngoscope':
        if supply['size']=="1":
            supply['is_available']=True

        
tasks=[]
for supply in supplyList:
    task={
        'name':'fetch',
        'supply_name':supply['name'],
        'size':supply['size'],
        'pp':'fetch '+supply['pp']
    }
    tasks.append(task)
for supply in supplyList:
    task={
        'name':'use',
        'supply_name':supply['name'],
        'size':supply['size'],
        'pp':'use '+supply['pp']
    }
    tasks.append(task)

simpleTasks=[
    "dry",
    "stimulate",
    "bulb_suction",
    "deep_suction"
]
for taskName in simpleTasks:
    task={
        'name':taskName,
        'pp':taskName
    }
    tasks.append(task)