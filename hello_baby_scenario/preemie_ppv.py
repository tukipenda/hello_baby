from scenario import *
from baby_update import BabyUpdate


# probably should move all of below into its own scenario data page - or maybe even preemieppv scenario page


#PreemiePPV scenario - data and logic
#initial data about infant - all of this should probably be in the form of objects to make life easier
initVitals={'O2Sat':55, 'HR':120, 'RR':40, 'SBP':75, 'DBP':50, 'Temp':35, 'weight':2.25} # weight probably belongs somewhere else
initAPGAR={"tone":0, "cry":1, "color":1, "respirations":1, "HR":2}
initResp={"rate":initVitals['RR'], "breath_sounds":"None", "chest_rise":"None", "WOB":"None", "grunting?":"None", "spontaneous?":"False"}
initCardiac={"HR":initVitals['HR'], "murmur":"no murmur", "femoral_pulse":"2+", "radial_pulse":"2+"}
initAbd={"BS":"+bs", "palpate":"soft, no HSM"}
initSkin={"color":initAPGAR['color'], "dry?":False, "texture":"term infant skin"}
initOtherPE={"scalp":'no caput', "clavicles":'no clavicular fracture', "ears":'normally positioned', 
             "eyes":'red reflex intact bilaterally', "umbilical_cord":"normal 3 vessel cord", "palate":'palate intact', "lips":'no cleft lips', "GU":'normal genitalia', 
             "hips":'no hip click', "spine":'no dimple', "anus":'patent anus'}

#internal_state
initSecretions={"quantity":'moderate', "below_cords":'no', "color":'clear', "thickness":'thin'}
initNeuro={"LOC":'weak cry', "RLeg":'moving normally', "LLeg":'moving normally', "RArm":'moving normally', "LArm":'moving normally', "deficit":"none"}
initSats={"RArm":initVitals['O2Sat'], "LArm":initVitals['O2Sat'], "RLeg":initVitals['O2Sat'], "LLeg":initVitals['O2Sat']}
#initBP={"RArm":{}, "LArm":{}, "RLeg":{}, "LLeg":{}}
initEKG={"Rhythm":'sinus'}
initMalformations={} #may need to change this to a list
PEdict={'apgar':initAPGAR, 'resp':initResp, 'cardiac':initCardiac, 'abd':initAbd, 'skin':initSkin, 'otherPE':initOtherPE, 
        'secretions':initSecretions, 'neuro':initNeuro, 'sats':initSats, 'ekg':initEKG, 'malformations':initMalformations}


class PreemiePPVUpdate(BabyUpdate):
    def __init__(self, baby, warmer, supplyMGR):
        super().__init__(baby, warmer, supplyMGR)

    def loadData(self):
        super().loadData(initVitals, PEdict)
        
    def updateResp(self, *args, **kwargs):
        resp=self.PE['resp']
        if False: #replace w/ getting effective ventilation?
#            self.PE['resp']['rate']=ventilation.rate
#           self.PE['resp]
            pass
        
        elif self.time<60:
            resp['breath_sounds']="None"
            resp['WOB']="None"
            resp['grunting']=False
            resp['spontaneous']=False
            resp['chest_rise']="None"
            resp['rate']=0
            self.vitals['RR']=0
        
        elif self.time<120:
            pass


class PreemiePPVScenario(Scenario):
    def __init__(self):
        super().__init__()

    def loadData(self):
        self.scenario_data={'scenario_text':"You are called by the OB team for a stat C/S. Mom is 25 years old, and gestational age is 32 weeks."}
        pL="Prenatal labs: VZVI, RI, HIV negative, Hep B negative, RPRNR, GC/Chlamydia negative"
        hsv="No history of HSV and has no active lesions."
        gbs="GBS+.  She was febrile to 38.1, and received ampicillin 2 hours before delivery."
        rom="ROM occurred 16 hours ago."
        gp="G1PO"
        self.mom=Mom(age=25, prenatalLabs=pL, HSV=hsv, GBS=gbs, ROM=rom, GP=gp)

        self.mom=Mom(age=25, prenatalLabs=pL, HSV=hsv, GBS=gbs, ROM=rom, GP=gp)

        nurse=staff.RN("Juan")
        respiratory=staff.RT("Sheri")
        self.staff=staff.Staff([nurse, respiratory])


        supplyList=[
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
        loadSupplyList={"laryngoscope":[], "ETT":[], "mask":[]}
        for supplyName in supplyList:
            supply=supplies.Supply(supplyName)
            loadSupplyList[supplyName]=supply

        for size in ["0", "1", "00"]:
            laryngoscope=supplies.Laryngoscope(size)
            loadSupplyList["laryngoscope"].append(laryngoscope)

        for size in ["2.5", "3", "3.5", "4"]:
            ETT=supplies.ETT(size)
            loadSupplyList["ETT"].append(ETT)

        for maskType in ["Infant", "Preemie"]:
            mask=supplies.Mask(maskType)
            loadSupplyList["mask"].append(mask)

        baby=Baby(32, [])
        self.baby=baby
        super().loadData(loadSupplyList, baby)
        self.supplyMGR=supplies.SupplyManager(loadSupplyList)
        self.tasks={
            'fetch':self.supplyMGR.fetchSupply,
            'place':self.supplyMGR.placeSupply,
            'turnOn':self.warmer.turnOn
       #    'dry':,
        #    'stimulate':,
         #   'suction':,
            
        }



    def loadBabyUpdate(self):
        self.babyUpdate=PreemiePPVUpdate(self.baby, self.warmer, self.supplyMGR)
        self.babyUpdate.loadData()

# temperature (turned on), suction, bag/mask, oxygen flow, baby timer
# supplies - ETT (sizes), masks, pulse ox, laryngoscope, hat, blankets, bulb suction, deep suction/meconium aspirator, preemie supplies
