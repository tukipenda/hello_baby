from baby import *

#need to write tests for all of these methods!!!

class BabyUpdate:
    def __init__(self, baby, warmer, supplyMGR):
        self.baby=baby
        self.PE={}
        self.vitals={}
        self.warmer=warmer
        self.supplyMGR=supplyMGR
        self.activeTasks=[]
        self.time=0

    def loadData(self, vitals, PE):
        self.baby.initialize(vitals, PE)
        self.PE=self.baby.PE
        self.vitals=self.baby.vitals


    def update(self, *args, **kwargs):
        if 'time' in kwargs.keys():
            self.time=kwargs['time']
        if 'taskname' in kwargs.keys():
            self.currentTaskName=kwargs['taskname']
        else:
            self.currentTaskName=None
        self.updateVitals(*args, **kwargs)
        self.updateApgar(*args, **kwargs)
        self.updateCardiac(*args, **kwargs)
        self.updateResp(*args, **kwargs)
        self.updateNeuro(*args, **kwargs)
        self.updateSecretions(*args, **kwargs)
        self.updateSats(*args, **kwargs)
        self.updateEKG(*args, **kwargs)
        self.updateSkin(*args, **kwargs)


    def updateVitals(self, *args, **kwargs):
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

    def updateApgar(self, *args, **kwargs):
        pass

    def updateResp(self, *args, **kwargs):
        pass
        

    def updateCardiac(self, *args, **kwargs):
        pass

    def updateSecretions(self, *args, **kwargs):
        pass

    def updateNeuro(self, *args, **kwargs):
        pass

    def updateSats(self, *args, **kwargs):
        pass

    def updateSkin(self, *args, **kwargs):
        if self.currentTaskName=="dry":
            self.baby.PE['skin']['dry?']=True

    def updateEKG(self, *args, **kwargs):
        pass