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
		self.cmdDict={"setO2":self.setOxygenString, "setSuction":self.setSuction, "setTemp":self.setTempMode, "turnOn":self.turnOn, "printWarmer":self.printWarmerStatus}

	def turnOn(self):
		self.turnedOn=True
	
	def setOxygen(self, flow, FIO2):
		self.flow=flow
		self.FIO2=FIO2
	
	def setOxygenString(self):
		self.flow=input("Flow: ")
		self.FIO2=input("FIO2: ")
		self.setOxygen(self.flow, self.FIO2)

	def setSuction(self, suction):
		self.suction=suction
	
	def setTempMode(self, tempMode):
		self.tempMode=tempMode
			
	def __str__(self):
		return self.printWarmerStatus()
	
	def printWarmerStatus(self):
		toPrint=""
		onStatus="off"
		if self.turnedOn:
			onStatus="on"
			toPrint+="Warmer is "+onStatus+"."
		if(self.flow==0):
			toPrint+="\nOxygen is not turned on"
		else:
			toPrint+="\nOxygen is set at "+str(self.flow)+" L of flow with an FiO2 of "+str(self.FIO2)+"%"
		if(self.suction==0):
			toPrint+="\nSuction is not turned on"
		else:
			toPrint+="\nSuction is set at "+str(self.suction)
		print(toPrint)
		return(toPrint)
