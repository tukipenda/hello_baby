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
	def __init__(self, taskName, baby, warmer, duration):
		self.taskName=taskName
		self.startTime=None
		self.baby=baby
		self.duration=duration
		self.message=""
		self.isSuccessful=None
		self.isComplete=None
		self.isStarted=None
		self.warmer=warmer
	
	def doTask(self, startTime, staffmember):
		self.isStarted=True
		self.startTime=startTime
	
	def succeeds(self, scenario):
		self.isSuccessful=True
		return self.isSuccessful

	def complete(self, time, scenario, *args):
		self.succeeds(scenario)


class FetchSupply(Task):
	def __init__(self, taskName, baby, warmer, duration):
		super().__init__(taskName, baby, warmer, duration)
		
	def complete(self, supplyName):
		self.warmer.getSupply(supplyName)
	
	

class PlaceSupply(Task):
	def __init__(self, taskName, baby, warmer, duration):
		super().__init__(taskName, baby, warmer, duration)

class InterveneTask(Task):
	def __init__(self, taskName, baby, warmer, duration):
		super().__init__(taskName, baby, warmer, duration)

	def doTask(self, startTime, staffmember, *args):
		super().doTask(self)
	
	def complete(self, time, scenario, *args):
		super().complete(time, scenario)
		self.isComplete=True
		scenario.babyUpdate.update(self.taskName, self.isSuccessful, time)
		
class Intubate(InterveneTask):
	pass

class PlaceUVC(InterveneTask):
	pass

class GivePPV(InterveneTask):
	pass

class GiveMed(InterveneTask):
	pass

class Suction(InterveneTask):
	pass

class CPR(InterveneTask):
	pass


#other interventions - adjust mask, increase PPV, open mouth, suction (location of suctioning, type)
#warm, dry, stim, place UVC, give EPI (dose, route), give NS bolus, give below_cords
#ask OBs for delayed cord clamping

allTasks=[
	["dry", 10],
	["intubate", 15], #needs parameters
	["givePPV", 5] #needs parameters, startTime/endTime
]

taskData={}
for task in allTasks:
	taskData[task[0]]={"name":task[0], "duration":task[1]}
	

class TaskManager(JSONClass):
	def __init__(self, warmer, baby, scenario):
		self.baby=baby
		self.warmer=warmer
		self.taskList={}
		self.tasks=[]
		self.cmdDict={'listTasks':self.listTasks}
		self.scenario=scenario
		self.tasksToLoad=taskData
	
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
		self.taskList["fetch"]=FetchSupply("fetch", self.baby, self.warmer, 5)
		self.taskList["place"]=PlaceSupply("place", self.baby, self.warmer, 5)
		for task in self.tasksToLoad.keys():
			taskData=self.tasksToLoad[task]
			self.taskList[task]=InterveneTask(taskData['name'], self.baby, self.warmer, taskData['duration'])
		
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
