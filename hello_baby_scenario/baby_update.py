from baby import *

#need to write tests for all of these methods!!!

class BabyUpdate:
    def __init__(self, baby, warmer, supplyMGR):
        self.baby=baby
        self.warmer=warmer
        self.supplyMGR=supplyMGR
        self.activeTasks=[]

    def loadData(self, vitals, PE):
        self.baby.initialize(vitals, PE)

    def update(self, *args):
        self.updateVitals(*args)
        self.updateApgar(*args)
        self.updateCardiac(*args)
        self.updateResp(*args)
        self.updateNeuro(*args)
        self.updateSecretions(*args)
        self.updateSats(*args)
        self.updateEKG(*args)
        self.updateSkin(*args)


    def updateVitals(self, taskName, isSuccessful, time):
        def updateHR():
            pass
        def updateRR():
            pass

        def updateTemp():
            temp=self.baby.vitals['Temp']
            #if warmer not on, lose 0.05 C every 5 seconds until temp is 33
            #if warmer on and hat on, baby dry, GA high enough, gain 0.1 C every 5 seconds until temp is 37 (if baby mode is on)
            #if baby mode is off, temp keeps increasing to 39
            # if hat not on, baby not dry - temp stays at 35
            if not self.warmer.turnedOn:
                if temp>33:
                    self.baby.vitals['Temp']=round(temp-0.05, 2)
            else:
                if ((self.baby.PE['skin']['dry?']) and (self.baby.has("hat"))):
                    if (self.warmer.tempMode=="manual" or temp<37):
                        self.baby.vitals['Temp']=round(temp+0.05, 2)
                    if (self.warmer.tempMode=="baby" and temp>37):
                        self.baby.vitals['Temp']=round(temp-0.05, 2)
                else:
                    if temp>34:
                        self.baby.vitals['Temp']=round(temp-0.05, 2)




        def updateO2sat():
            pass

        updateHR()
        updateRR()
        updateTemp()
        updateO2sat()

    def updateApgar(self, taskName, isSuccessful, time):
        pass

    def updateResp(self, taskName, isSuccessful, time):
        pass

    def updateCardiac(self, taskName, isSuccessful, time):
        pass

    def updateSecretions(self, taskName, isSuccessful, time):
        pass

    def updateNeuro(self, taskName, isSuccessful, time):
        pass

    def updateSats(self, taskName, isSuccessful, time):
        pass

    def updateSkin(self, taskName, isSuccessful, time):
        if taskName=="dry":
            self.baby.PE['skin']['dry?']=True

    def updateEKG(self, taskName, isSuccessful, time):
        pass


# probably should move all of below into its own scenario data page - or maybe even preemieppv scenario page

#PreemiePPV scenario - data and logic
#initial data about infant
initVitals={'O2Sat':55, 'HR':120, 'RR':40, 'SBP':75, 'DBP':50, 'Temp':35}
initAPGAR={"tone":0, "cry":1, "color":1, "respirations":1, "HR":2}
initResp={"rate":initVitals['RR'], "breath_sounds":"None", "chest_rise":"None", "WOB":"None", "grunting?":"None", "spontaneous?":"False"}
initCardiac={"HR":initVitals['HR'], "murmur":"no murmur", "femoral_pulse":"2+", "radial_pulse":"2+"}
initAbd={"BS":"+bs", "palpate":"soft, no HSM"}
initSkin={"color":initAPGAR['color'], "dry?":False, "texture":"term infant skin"}
initOtherPE={"scalp":'no caput', "clavicles":'no clavicular fracture', "ears":'normally positioned', "eyes":'red reflex intact bilaterally', "umbilical_cord":"normal 3 vessel cord", "palate":'palate intact', "lips":'no cleft lips', "GU":'normal genitalia', "hips":'no hip click', "spine":'no dimple', "anus":'patent anus'}

#internal_state
initSecretions={"quantity":'moderate', "below_cords":'no', "color":'clear', "thickness":'thin'}
initNeuro={"LOC":'weak cry', "RLeg":'moving normally', "LLeg":'moving normally', "RArm":'moving normally', "LArm":'moving normally', "deficit":"none"}
initSats={"RArm":initVitals['O2Sat'], "LArm":initVitals['O2Sat'], "RLeg":initVitals['O2Sat'], "LLeg":initVitals['O2Sat']}
#initBP={"RArm":{}, "LArm":{}, "RLeg":{}, "LLeg":{}}
initEKG={"Rhythm":'sinus'}
initMalformations={} #may need to change this to a list
PEdict={'apgar':initAPGAR, 'resp':initResp, 'cardiac':initCardiac, 'abd':initAbd, 'skin':initSkin, 'otherPE':initOtherPE, 'secretions':initSecretions, 'neuro':initNeuro, 'sats':initSats, 'ekg':initEKG, 'malformations':initMalformations}


class PreemiePPV(BabyUpdate):
    def __init__(self, baby, warmer, supplyMGR):
        super().__init__(baby, warmer, supplyMGR)

    def loadData(self):
        super().loadData(initVitals, PEdict)
