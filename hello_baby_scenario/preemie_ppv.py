from scenario import *
from baby_update import *
from jsonclass import simple_tree

#I deleted APGAR for now,not including malformations, BP, EKG, or 4-extremity sats
PE=simple_tree()
PE['vitals']={'O2Sat':55, 'HR':120, 'RR':40, 'SBP':75, 'DBP':50, 'temp':35, 'weight':2.25}
PE['resp']={"breath_sounds":"None", "chest_rise":"None", "WOB":"None", "grunting?":"None", "spontaneous?":"False"}
PE['cardiac']={"murmur":"no murmur", "femoral_pulse":"2+", "radial_pulse":"2+"}
PE['abd']={"BS":"+bs", "palpate":"soft, no HSM"}
PE['skin']={"color":'blue', "dry?":False, "texture":"term infant skin"}
PE['secretions']={"quantity":'moderate', "below_cords":'no', "color":'clear', "thickness":'thin'}
PE['neuro']={"LOC":'weak cry', "RLeg":'moving normally', "LLeg":'moving normally', "RArm":'moving normally', "LArm":'moving normally', "deficit":"none"}
PE['other']={"scalp":'no caput', "clavicles":'no clavicular fracture', "ears":'normally positioned',
             "eyes":'red reflex intact bilaterally', "umbilical_cord":"normal 3 vessel cord", "palate":'palate intact', "lips":'no cleft lips', "GU":'normal genitalia',
             "hips":'no hip click', "spine":'no dimple', "anus":'patent anus'}


def test_first():
    assert 1+2==3

class PreemiePPVHealth(Health):
    def __init__(self, baby, vent, CPR, UVC):
        circ_eff=3
        vol_status=3
        card_health=3
        brain_health=3
        super().__init__(baby, vent, CPR, UVC, circ_eff, vol_status, card_health, brain_health)

    def updateCardiac(self, time):
        O2del=self.getO2Delivery()
        if time>60:
            goodO2Del=sum(O2Del[-12:]) #seconds of good O2 delivery in the last minute
            if (time-self.timeChanged)>60:
                if (goodO2Del<15):
                    self.card_health=max(0, self.card_health-1)
                    self.timeChanged=time
                # need to fix the case where time<120
                elif(sum(O2Del[-24:])<45 and goodO2Del<30): #if we've only had 30 seconds of good O2 in the past minute, and 45 in the past two minutes, we are in trouble.
                    self.card_health=max(0, self.card_health-1)
                    self.timeChanged=time
            elif goodO2Del>55:
                self.card_health=min(3, self.card_health+1)
                self.timeChanged=time



class PreemiePPVUpdate(BabyUpdate):
    def __init__(self, baby, health, warmer, supplyMGR):
        super().__init__(baby, health, warmer, supplyMGR)

    def loadData(self):
        super().loadData(PE)

    def updateResp(self, *args, **kwargs):
        resp=self.PE['resp']
        vent=self.vent
        if vent.type in ["mechanical", "PPV"]:
            resp.rate=vent.rate
            resp.breath_sounds="clear bilaterally"
            resp.grunting="None"
            if vent.efficacy=="good":
                resp.chest_rise="good"
            if vent.efficacy=="poor":
                resp.chest_rise="minimal chest rise"
                resp.breath_sounds="barely audible"
            if vent.efficacy=="none":
                resp.chest_rise="none"
                resp.breath_sounds="None"

        elif vent.type=="spontaneous":
            pass

        else:
            resp['breath_sounds']="None"
            resp['WOB']="None"
            resp['grunting']=False
            resp['spontaneous']=False
            resp['chest_rise']="None"
            resp['rate']=0
            self.vitals['RR']=0

    def updateCardiac(self, *args, **kwargs):
        pass

    def updateVitals(self, *args, **kwargs):
        pass

    def updateNeuro(self, *args, **kwargs):
        pass

    def updateSecretions(self, *args, **kwargs):
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
            'turnOn':self.warmer.turnOn,
            'useMask':self.supplyMGR.useMask,
       #    'dry':,
        #    'stimulate':,
         #   'suction':,

        }



    def loadBabyUpdate(self):
        self.vent=Ventilation(self.warmer)
        self.CPR=CPR()
        self.UVC=UVC()
        self.health=PreemiePPVHealth(self.baby, self.vent, self.CPR, self.UVC)
        self.babyUpdate=PreemiePPVUpdate(self.baby, self.health, self.warmer, self.supplyMGR)
        self.babyUpdate.loadData()

# temperature (turned on), suction, bag/mask, oxygen flow, baby timer
# supplies - ETT (sizes), masks, pulse ox, laryngoscope, hat, blankets, bulb suction, deep suction/meconium aspirator, preemie supplies
