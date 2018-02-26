#my approach to supplies sucks at the moment


# dry/stimulate
# provide oxygen (adjust mask, troubleshoot ETT)
# give CPR - who is doing it, rate, depth, pausing? (correct compressions if needed)
# place equipment, place UVC/PIV, cardiac leads.
# give medication (estimate weight by GA)
# each intervention takes a certain amount of time to perform
# give blood

#PPV - needs to be a continuous action

# intervention - has actor, duration of time, baby that it manipulates
from jsonclass import *

class Task(JSONClass):
    def __init__(self, taskName, baby, supplyMGR):
        self.taskName=taskName
        self.startTime=None
        self.baby=baby
        self.message=""
        self.isSuccessful=None
        self.isComplete=None
        self.isStarted=None
        self.supplyMGR=supplyMGR

    def doTask(self):
        pass


class FetchSupply(Task):
    def __init__(self, baby, supplyMGR):
        super().__init__("fetch", baby, supplyMGR)

    def doTask(self, supplyName, **kwargs):
        self.supplyMGR.fetchSupply(supplyName, **kwargs)


class PlaceSupply(Task):
    def __init__(self, baby, supplyMGR):
        super().__init__("place", baby, supplyMGR)

    def doTask(self, supplyName, **kwargs):
        supply=self.supplyMGR.getSupply(supplyName, **kwargs)
        if supply:
            supply.using=True
            self.supplyMGR.placeSupply(supplyName, **kwargs)


class UseMask(Task):
    def __init__(self, baby, supplyMGR):
        super().__init__("usemask", baby, supplyMGR)

    def doTask(self, masktype):
        self.supplyMGR.fetchSupply("mask", masktype)

#need to make this more accurate
class PlaceUVC(PlaceSupply):
    def __init__(self, baby, supplyMGR):
        super().__init__(baby, supplyMGR)

    def doTask(self, **kwargs):
        super().doTask("UVC", **kwargs)


class InterveneTask(Task):
    def __init__(self, taskName, baby, supplyMGR):
        super().__init__(taskName, baby, supplyMGR)

    def doTask(self, *args):
        super().doTask(self)

class Intubate(InterveneTask):
    def __init__(self, baby, supplyMGR):
        super().__init__("intubate", baby, supplyMGR)

#MR SOPA adjustments - change pressures elsewhere, suction is a different one, as is airway adjunct
# also need to updated baby based on efficacy of PPV.
class GivePPV(Task):
    def __init__(self, baby, supplyMGR):
        super().__init__("givePPV", baby, supplyMGR)

        #self.airLeak=False - should be a property of the mask instead

    def startPPV(self, startTime, *args):
        pass

    def stopPPV(self, endTime):
        pass

    def adjustMask(self):
        pass

    def openMouth(self):
        pass

    def repositionBaby(self):
        pass

class GiveMed(InterveneTask):
    def __init__(self, baby, supplyMGR):
        super().__init__("giveMed", baby, supplyMGR)

class Suction(InterveneTask):
    def __init__(self, baby, supplyMGR, duration):
        super().__init__("suction", baby, supplyMGR)

class CPR(InterveneTask):
    def __init__(self, baby, supplyMGR):
        super().__init__("cpr", baby, supplyMGR)

    def startCPR(self):
        pass

    def stopCPR(self):
        pass


#other interventions - adjust mask, increase PPV, open mouth, suction (location of suctioning, type)
#warm, dry, stim, place UVC, give EPI (dose, route), give NS bolus, give below_cords
#ask OBs for delayed cord clamping

# need to add staff to this at some point
class TaskManager(JSONClass):
    def __init__(self, supplyMGR, baby, scenario):
        self.baby=baby
        self.supplyMGR=supplyMGR
        self.taskList={}
        self.scenario=scenario

    def doTask(self, taskName, *args):
        task=self.taskList[taskName]
        task.doTask(*args)

    def loadTasks(self):
        self.taskList["fetch"]=FetchSupply(self.baby, self.supplyMGR)
        self.taskList["use"]=FetchSupply(self.baby, self.supplyMGR)
        self.taskList["place"]=PlaceSupply(self.baby, self.supplyMGR)
        self.taskList["placeUVC"]=PlaceUVC(self.baby, self.supplyMGR)
        self.taskList["dry"]=InterveneTask("dry", self.baby, self.supplyMGR)
        self.taskList["stim"]=InterveneTask("stim", self.baby, self.supplyMGR)
        self.taskList["giveMed"]=GiveMed(self.baby, self.supplyMGR)
        self.taskList["intubate"]=Intubate(self.baby, self.supplyMGR)
        self.taskList["suction"]=Suction(self.baby, self.supplyMGR)
        self.taskList["givePPV"]=GivePPV(self.baby, self.supplyMGR)
        self.taskList["cpr"]=CPR(self.baby, self.supplyMGR)