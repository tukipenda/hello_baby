from jsonclass import JSONClass

#At the moment, only ventilation and health need to be fully written out

class Baby(JSONClass):
    def __init__(self, ga, nc):
        super().__init__()
        self.ga=ga
        self.nc=nc
        self.vitals=None
        self.PE=None
        self.delivered=False
        self.supplies={}

    def initialize(self, PE):
        self.PE=PE
        self.vitals=PE['vitals']
        
    def deliver(self):
        self.delivered=True
    
    def has(supplyName):
        for supply in self.supplies:
            if suppy.name==supplyName:
                return True
        return False

#need to write tests for all of these methods!!!
class Ventilation(JSONClass):
    def __init__(self, warmer):
        self.warmer=warmer
        self.type="spontaneous"
        self.efficacy=None
        self.mouthOpen=True
        self.positioning=None
        self.airwayOpen=None
        self.airLeak=None        
        #self.rate, pressures, secretions, ETT type
        
    def startPPV(self):
        self.type="PPV"
    
    def stopPPV(self):
        self.type="spontaneous"
   
    def adjustMask(self):
        pass
    
    def openMouth(self):
        self.mouthOpen=True
    
    def reposition(self):
        pass
   
    def deepSuction(self):
        pass
    
    def setPressures(self, PIP, PEEP, POP):
        pass
    
    def intubate(self):
        self.type="mechanical"
   
    def extubate(self):
        self.type="PPV"
    
    def update(self, *args, **kwargs):
        pass
    

class CPR(JSONClass):
    def __init__(self):
        self.rate=0
        self.breathsToCompressions=None # [1, 3]
        self.CPRDepth=None #depth options are 1/6, 1/3, 1/2
        self.efficacy=None
    
    def startCPR(self, rate, BTC, depth):
        self.rate=rate
        self.breathsToCompressions=BTC
        self.CPRDepth=depth
    
    def stopCPR(self):
        self.rate=0
    
    def increaseDepth(self):
        pass
    
    def decreaseDepth(self):
        pass
   
    def setRate(self, rate):
        self.rate=rate
    
    def setRatio(self, depth):
        self.CPRDepth=depth
   
    def update(self, *args, **kwargs):
        pass
    
class UVC(JSONClass):
    def __init__(self):
        self.uvc_placed=False
        self.medicationsGiven=[]
    
    def placeUVC(self):
        self.uvc_placed=True
    
    def giveMed(self, medication, amount):
        pass
    
    def giveVolume(self, fluid, amount):
        pass
    
    def giveBlood(self, amount):
        pass
    
    def update(self, *args, **kwargs):
        pass

# circ_eff - 0-3 - 0 is none, 1 is poor, 2 is weak, 3 is excellent
# vol_status - 0-3 - 0 is severely decreased, 1 is moderately decreased, 2 is mildly decreased, 3 is normal
# card_health - 0-3 - (3 is the best)
# brain_health - 0-3 (this measure is probably too crude)

# eventually need to expand to include ventilation and oxygenation
    
class Health(JSONClass):
    def __init__(self, baby, vent, CPR, UVC, circ_eff, vol_status, card_health, brain_health):
        self.baby=baby
        self.vent=vent
        self.CPR=CPR
        self.UVC=UVC
        self.circ_eff=circ_eff #circulation efficacy
        
        self.oxygenation=[]
        self.circulation=[]
        self.ventilation=[]
        
        self.volume_status=vol_status
        self.card_health=card_health
        self.brain_health=brain_health
        self.timeChanged=0
    
    def update(self, time):
        self.updateO2(time)
        self.updateCirculation(time)
        self.updateCardiac(time)
        self.updateNeuro(time)
        
    def updateO2(self, time):
        ndelta=len(self.oxygenation)
        tdelta=time//5
        resp_eff=0
        if vent.efficacy==1:
            resp_eff=1
        if tdelta>ndelta:
            for x in range(len(tdelta-ndelta)):
                self.oxygenation.append(resp_eff)
    
    def updateCirculation(self, time):
        ndelta=len(self.circulation)
        tdelta=time//5
        if tdelta>ndelta:
            for x in range(len(tdelta-ndelta)):
                self.circulation.append(self.circ_eff)
    
    def getO2Delivery(self):
        return [5*ox*circ/3.0 for ox,circ in zip(self.oxygenation, self.circulation)]
    
    def updateCardiac(self, time):
        pass
    
    def updateNeuro(self, time):
        pass
                
        