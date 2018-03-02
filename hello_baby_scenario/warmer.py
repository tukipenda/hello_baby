from jsonclass import *
from supplies import *

# temperature (turned on), suction, bag/mask, oxygen flow, baby timer
# supplies - ETT (sizes), masks, pulse ox, laryngoscope, hat, blankets, bulb suction, deep suction/meconium aspirator, preemie supplies


class Warmer(JSONClass):
    def __init__(self):
        super().__init__()
        self.turnedOn=False
        self.suction=0
        self.flow=0
        self.FIO2=100
        self.tempMode="manual"
        self.PIP=0
        self.POP=0
        self.PEEP=0
      
    def turnOn(self):
        self.turnedOn=True
    
    def setOxygen(self, flow, FIO2):
        self.flow=flow
        self.FIO2=FIO2

        
    def setPressure(self, PIP, PEEP, POP):
        self.PIP=PIP
        self.PEEP=PEEP
        self.POP=POP

    def setSuction(self, suction):
        self.suction=suction
    
    def setTempMode(self, tempMode):
        self.tempMode=tempMode
