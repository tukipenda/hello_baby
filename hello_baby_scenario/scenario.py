from jsonclass import JSONClass, merge_dicts
from baby import *
import warmer
import staff
import supplies
import tasks
import threading
from baby_timer import *
import baby_update
import time

#probably should move this into scenario_data of some sort
class Mom(JSONClass):
	def __init__(self, **kwargs):
		super().__init__()
		self.data=kwargs

class Scenario(JSONClass):
	def __init__(self):
		self.baby=None
		self.mom=None
		self.staff=None
		self.warmer=None
		self.supplyMGR=None
		self.scenario_data=None
		self.taskMGR=None
		self.getCMDs=threading.Thread(name='getCMDs', target=self.getCMDs)
		self.update=threading.Thread(name='update', target=self.updateBabyStatus)
		self.prepComplete=False
		self.resusComplete=False
		self.babyUpdate=None
		self.babyTimer=BabyTimer()

	def loadData(self):
		# Initialize a scenario
		self.scenario_data={'scenario_text':"You are called by the OB team for a stat C/S. Mom is 25 years old, and gestational age is 36 weeks."}
		self.baby=Baby(33, [])

		pL="Prenatal labs: VZVI, RI, HIV negative, Hep B negative, RPRNR, GC/Chlamydia negative"
		hsv="No history of HSV and has no active lesions."
		gbs="GBS+.  She was febrile to 38.1, and received ampicillin 2 hours before delivery."
		rom="ROM occurred 16 hours ago."
		gp="G1PO"
		self.mom=Mom(age=25, prenatalLabs=pL, HSV=hsv, GBS=gbs, ROM=rom, GP=gp)

		nurse=staff.RN("Juan")
		respiratory=staff.RT("Sheri")
		self.staff=staff.Staff([nurse, respiratory])

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
			"UVC_kit"
		]
		loadSupplyList=[]
		for supplyName in supplyList:
			supply=supplies.Supply(supplyName)
			loadSupplyList.append(supply)

		for size in ["0", "1", "00"]:
			laryngoscope=supplies.Laryngoscope(size)
			loadSupplyList.append(laryngoscope)
			
		for size in ["2.5", "3", "3.5", "4"]:
			ETT=supplies.ETT(size)
			loadSupplyList.append(ETT)
		
		for maskType in ["infant", "preemie"]:
			mask=supplies.BagMask(maskType)
			loadSupplyList.append(mask)

# temperature (turned on), suction, bag/mask, oxygen flow, baby timer
# supplies - ETT (sizes), masks, pulse ox, laryngoscope, hat, blankets, bulb suction, deep suction/meconium aspirator, preemie supplies
		self.warmer=warmer.Warmer()
		self.supplyMGR=supplies.SupplyManager(loadSupplyList)

		self.babyUpdate=baby_update.PreemiePPV(self.baby, self.warmer, self.supplyMGR)
		self.babyUpdate.loadData()

		self.taskMGR=tasks.TaskManager(self.supplyMGR, self.baby, self)
		self.taskMGR.loadTasks()

	def executeCmd(self, cmdName, *args):
		cmdDict=merge_dicts(self.baby.cmdDict, self.mom.cmdDict, self.staff.cmdDict, self.warmer.cmdDict, self.supplies.cmdDict, self.taskMGR.cmdDict)
		if cmdName=="l":
			for cmd in cmdDict.keys():
				print(cmd)
		# should put in a try/except, but for now this is useful for debugging
		if cmdName in cmdDict.keys():
			print(*args)
			cmdDict[cmdName](*args)
		else:
			if cmdName in self.taskMGR.taskList.keys():
				self.taskMGR.taskList[cmdName].complete(*args)


	def prepWarmer(self):
		print("Prep the Warmer")
		self.run_loop(self.prepComplete)

	def resuscitation(self):
		self.baby.deliver()
		self.getCMDs.start()
		self.update.start()
		self.babyTimer.startTimer()
		print("Resuscitate the baby")

	def updateBabyStatus(self):
		while(not self.resusComplete):
			time.sleep(5)
			self.taskMGR.completeTasks(self.babyTimer.getElapsedTime())

	def getCMDs(self):
		self.run_loop(self.resusComplete)

	def scoring(self):
		pass

	def run_loop(self, condition):
		while(not condition):
			cmd=input("Enter command: ")
			if(cmd=="q"):
				condition=True
			else:
				cmds=cmd.split(" ")
				self.executeCmd(*cmds)
		result=False
		return result

