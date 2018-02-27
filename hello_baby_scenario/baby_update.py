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


    def updateVitals(self, *args):
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

    def updateApgar(self, *args):
        pass

    def updateResp(self, *args):
        pass

    def updateCardiac(self, *args):
        pass

    def updateSecretions(self, *args):
        pass

    def updateNeuro(self, *args):
        pass

    def updateSats(self, *args):
        pass

    def updateSkin(self, *args):
        pass
#        if taskName=="dry":
 #           self.baby.PE['skin']['dry?']=True

    def updateEKG(self, *args):
        pass