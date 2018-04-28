from baby import *
from jsonclass import *

class BabyUpdate:
    def __init__(self, baby, health, warmer, supplyMGR):
        self.baby=baby
        self.PE={}
        self.vitals={}
        self.health=health
        self.warmer=warmer
        self.supplyMGR=supplyMGR
        self.activeTasks=[]
        self.time=0
        self.currentTaskName=None

    def loadData(self, PE):
        self.baby.initialize(PE)
        self.PE=self.baby.PE
        self.vitals=self.PE['vitals']


    def update(self, time, taskname=None):
        self.time=time
        self.currentTaskName=taskname
        self.UVC.update(*args, **kwargs)
        self.CPR.update(*args, **kwargs)
        updateVitals()
        updateSkin()


    def updateVitals(self):
        def updateHR():
            pass
        def updateRR():
            pass

        def updateTemp():
            temp=self.baby.vitals['temp']
            #if warmer not on, lose 0.05 C every 5 seconds until temp is 33
            #if warmer on and hat on, baby dry, GA high enough, gain 0.1 C every 5 seconds until temp is 37 (if baby mode is on)
            #if baby mode is off, temp keeps increasing to 39
            # if hat not on, baby not dry - temp stays at 35
            if not self.warmer.turnedOn:
                if temp>33:
                    self.baby.vitals['temp']=round(temp-0.05, 2)
            else:
                if ((self.baby.PE['skin']['dry?']) and (self.baby.has("hat"))):
                    if (self.warmer.tempMode=="manual" or temp<37):
                        self.baby.vitals['temp']=round(temp+0.05, 2)
                    if (self.warmer.tempMode=="baby" and temp>37):
                        self.baby.vitals['temp']=round(temp-0.05, 2)
                else:
                    if temp>34:
                        self.baby.vitals['temp']=round(temp-0.05, 2)




        def updateO2sat():
            pass

        updateHR()
        updateRR()
        updateTemp()
        updateO2sat()

    def updateSkin(self):
        if self.currentTaskName=="dry":
            self.baby.PE['skin']['dry?']=True