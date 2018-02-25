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
	def __init__(self, taskName, baby, supplyMGR, duration):
		self.taskName=taskName
		self.startTime=None
		self.baby=baby
		self.duration=duration
		self.message=""
		self.isSuccessful=None
		self.isComplete=None
		self.isStarted=None
		self.supplyMGR=supplyMGR
	
	def doTask(self, startTime, staffmember):
		self.isStarted=True
		self.startTime=startTime
	
	def succeeds(self, scenario):
		self.isSuccessful=True
		return self.isSuccessful

	def complete(self, time, scenario, *args):
		self.succeeds(scenario)


class FetchSupply(Task):
	def __init__(self, baby, supplyMGR, duration):
		super().__init__("fetch", baby, supplyMGR, duration)
		
	def complete(self, supplyName, **kwargs):
		self.supplyMGR.fetchSupply(supplyName, **kwargs)
	

class PlaceSupply(Task):
	def __init__(self, baby, supplyMGR, duration):
		super().__init__("place", baby, supplyMGR, duration)
	
	def complete(self, supplyName, **kwargs):
		supply=self.supplyMGR.getSupply(supplyName, **kwargs)
		if supply:
			supply.using=True
			self.supplyMGR.placeSupply(supplyName, **kwargs)

#need to make this more accurate
class PlaceUVC(PlaceSupply):
	def __init__(self, baby, supplyMGR, duration):
		super().__init__(baby, supplyMGR, duration)
	
	def complete(self, **kwargs):
		super().complete("UVC", **kwargs)
			
			
class InterveneTask(Task):
	def __init__(self, taskName, baby, supplyMGR, duration):
		super().__init__(taskName, baby, supplyMGR, duration)

	def doTask(self, startTime, staffmember, *args):
		super().doTask(self)
	
	def complete(self, time, scenario, *args):
		super().complete(time, scenario)
		self.isComplete=True
		scenario.babyUpdate.update(self.taskName, self.isSuccessful, time)
		
class Intubate(InterveneTask):
	def __init__(self, baby, supplyMGR, duration):
		super().__init__("intubate", baby, supplyMGR, duration)	

#MR SOPA adjustments - change pressures elsewhere, suction is a different one, as is airway adjunct
# also need to updated baby based on efficacy of PPV.
class GivePPV(Task):
	def __init__(self, baby, supplyMGR, duration):
		super().__init__("givePPV", baby, supplyMGR, duration)
		
		#self.airLeak=False - should be a property of the mask instead
	
	def startPPV(self, startTime, staffmember, *args):
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
	def __init__(self, baby, supplyMGR, duration):
		super().__init__("giveMed", baby, supplyMGR, duration)

class Suction(InterveneTask):
	def __init__(self, baby, supplyMGR, duration):
		super().__init__("suction", baby, supplyMGR, duration)

class CPR(InterveneTask):
	def __init__(self, baby, supplyMGR, duration):
		super().__init__("cpr", baby, supplyMGR, duration)
	
	def startCPR(self):
		pass
	
	def stopCPR(self):
		pass


#other interventions - adjust mask, increase PPV, open mouth, suction (location of suctioning, type)
#warm, dry, stim, place UVC, give EPI (dose, route), give NS bolus, give below_cords
#ask OBs for delayed cord clamping	

class TaskManager(JSONClass):
	def __init__(self, supplyMGR, baby, scenario):
		self.baby=baby
		self.supplyMGR=supplyMGR
		self.taskList={}
		self.tasks=[]
		self.cmdDict={'listTasks':self.listTasks}
		self.scenario=scenario
	
	def doTask(self, taskName, staffmember, startTime):
		task=self.getTaskByName(taskName)
		if task:
			task.doTask(staffmember, startTime)
			self.tasks.append(task)
			return task
		else:
			#need to raise error
			return None
	
	def loadTasks(self):
		self.taskList["fetch"]=FetchSupply(self.baby, self.supplyMGR, 5)
		self.taskList["place"]=PlaceSupply(self.baby, self.supplyMGR, 5)
		self.taskList["placeUVC"]=PlaceUVC(self.baby, self.supplyMGR, 15)
		self.taskList["dry"]=InterveneTask("dry", self.baby, self.supplyMGR, 5)
		self.taskList["stim"]=InterveneTask("stim", self.baby, self.supplyMGR, 5)
		self.taskList["giveMed"]=GiveMed(self.baby, self.supplyMGR, 15)
		self.taskList["intubate"]=Intubate(self.baby, self.supplyMGR, 15)
		self.taskList["suction"]=Suction(self.baby, self.supplyMGR, 5)
		self.taskList["givePPV"]=GivePPV(self.baby, self.supplyMGR, 5)
		self.taskList["cpr"]=CPR(self.baby, self.supplyMGR, 5)
		
	def getTaskByName(self, taskName):
		if (taskName, task in self.taskList.items()):
			return task
		else:
			return None
  
	def completeTasks(self, currentTime):
		if len(self.tasks)==0:
			self.scenario.babyUpdate.update("", True, currentTime)
		else:
			for task in self.tasks:
				if currentTime>(task.startTime+task.duration):
					task.complete(time, scenario)
	
	def listTasks(self):
		for taskName in self.taskList.keys():
			print(taskName)
