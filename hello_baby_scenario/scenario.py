from jsonclass import JSONClass
import patients
import warmer
import staff
import tasks
import threading
from baby_timer import *
import baby_update
import time

class Scenario(JSONClass):
	def __init__(self):
		self.baby=None
		self.mom=None
		self.staff=None
		self.warmer=None
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
		self.baby=patients.Baby(33, [])

		pL=patients.prenatalLabs("VZVI", "RI", "HIV negative", "Hep B negative", "RPRNR", "Gonorrhea negative", "Chlamydia negative")
		hsv=patients.HSVStatus(False, False, False)
		gbs=patients.GBSStatus(True, 38.1, ["ampicillin"], False)
		rom=patients.ROM(16, False)
		gp=patients.GP(1, 0, 0, 0, 0, 0, 1)
		self.mom=patients.Mom(25, pL, hsv, gbs, [], rom, ["ampicillin"], gp)
		self.delivery=patients.Delivery("C/S", 1)

		nurse=staff.RN("Juan")
		respiratory=staff.RT("Sheri")
		self.staff=staff.Staff([nurse, respiratory])

		supplyList=[
			"ETT",
			"pulse_ox",
			"hat",
			"transwarmer",
			"plastic_bag",
			"temp_probe",
			"laryngoscope",
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
			supply=warmer.Supply(supplyName)
			loadSupplyList.append(supply)


# temperature (turned on), suction, bag/mask, oxygen flow, baby timer
# supplies - ETT (sizes), masks, pulse ox, laryngoscope, hat, blankets, bulb suction, deep suction/meconium aspirator, preemie supplies
		self.warmer=warmer.Warmer(loadSupplyList)

		self.babyUpdate=baby_update.PreemiePPV(self.baby, self.warmer)
		self.babyUpdate.loadData()

		self.taskMGR=tasks.TaskManager(self.warmer, self.baby, self)
		self.taskMGR.loadTasks()

	def executeCmd(self, cmdName, *args):
		cmdDict={**self.baby.cmdDict, **self.mom.cmdDict, **self.staff.cmdDict, **self.warmer.cmdDict, **self.taskMGR.cmdDict}
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

