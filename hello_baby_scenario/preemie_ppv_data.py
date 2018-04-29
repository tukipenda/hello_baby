scenario="You are called by the OB team for a stat C/S. Mom is 25 years old, and gestational age is 32 weeks."
baby_data={"ga":"32", "neonatal_complications":"None", "delivery":"C/S"}

mom_data={"age":25,
  "PNL":"Prenatal labs: VZVI, RI, HIV negative, Hep B negative, RPRNR, GC/Chlamydia negative",
"hsv":"No history of HSV and has no active lesions.",
  "gbs":"GBS+.  She was febrile to 38.1, and received ampicillin 2 hours before delivery.",
  "rom":"ROM occurred 16 hours ago.",
  "gp":"G1PO"}

vitals={'o2sat':55, 'hr':120, 'rr':40, 'sbp':75, 'dbp':50, 'temp':35, 'weight':2.25}
resp={"breath_sounds":"None", "chest_rise":"None", "wob":"None", "is_grunting":False, "is_spontaneous":False}
cardiac={"murmur":"no murmur", "femoral_pulse":"2+", "brachial_pulse":"2+"}
abd={"bs":"+bs", "palpate":"soft, no HSM"}
skin={"color":'blue', "is_dry":False, "texture":"term infant skin"}
secretions={"quantity":'moderate', "below_cords":False, "color":'clear', "thickness":'thin'}
neuro={"loc":'weak cry', "motor_deficit":"none"}
other={"scalp":'no caput', "clavicles":'no clavicular fracture', "ears":'normally positioned',
             "eyes":'red reflex intact bilaterally', "umbilical_cord":"normal 3 vessel cord", "palate":'palate intact', "lips":'no cleft lips', "gu":'normal genitalia',
             "hips":'no hip click', "spine":'no dimple', "anus":'patent anus'}

PE={"vitals":vitals, "resp":resp, "cardiac":cardiac, "abd":abd, "skin":skin, "secretions":secretions, "neuro":neuro, "other":other}

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
for supply in supplies:
    supplyList.append({"name":supply, "size":None})

for size in ["0", "1", "00"]:
    supplyList.append({"name":'laryngoscope', "size":size})

for size in ["2.5", "3", "3.5", "4"]:
    supplyList.append({"name":'ett', "size":size})

for maskType in ["Infant", "Preemie"]:
    supplyList.append({"name":'mask', "size":size})
