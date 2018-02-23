from jsonclass import *
from supplies import *

# temperature (turned on), suction, bag/mask, oxygen flow, baby timer
# supplies - ETT (sizes), masks, pulse ox, laryngoscope, hat, blankets, bulb suction, deep suction/meconium aspirator, preemie supplies


class Warmer(JSONClass):
	def __init__(self, supplies):
		super().__init__()
		self.turnedOn=False
		self.supplies=supplies
		self.suction=0
		self.flow=0
		self.FIO2=100
		self.tempMode="manual"
		self.mask=BagMask()
		self.cmdDict={"setO2":self.setOxygenString, "setSuction":self.setSuction, "setTemp":self.setTempMode, "turnOn":self.turnOn, "getSupply":self.getSupply,"printWarmer":self.printWarmerStatus, "printSupplyList":(lambda :print([supply.name for supply in self.supplies]))
		}
		self.cmdDict=merge_dicts(self.cmdDict, self.mask.cmdDict)

	def turnOn(self):
		self.turnedOn=True

	def setBagMask(self, maskType):
		self.mask.setMaskType(maskType)
	
	def setBagMaskPressures(self, PIP, PEEP, POP):
		self.mask.setPressures(PIP, PEEP, POP)
	
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
	
	def fetchSupply(self, name):
		success=False
		for supply in self.supplies:
			if supply.name==name:
				supply.available=True
				success=True
		if not success:
			print(name+" is unavailable.")
	
	def getSupply(self, name):
		toReturn=None
		for supply in self.supplies:
			if ((supply.name==name) and (supply.available)):
				toReturn=supply
		return toReturn
			
	def __str__(self):
		return self.printWarmerStatus()
	
	def printWarmerStatus(self):
		toPrint=""
		onStatus="off"
		if self.turnedOn:
			onStatus="on"
			toPrint+="Warmer is "+onStatus+"."
		toPrint+=str(self.mask)
		if(self.flow==0):
			toPrint+="\nOxygen is not turned on"
		else:
			toPrint+="\nOxygen is set at "+str(self.flow)+" L of flow with an FiO2 of "+str(self.FIO2)+"%"
		if(self.suction==0):
			toPrint+="\nSuction is not turned on"
		else:
			toPrint+="\nSuction is set at "+str(self.suction)
		toPrint+="\nSupplies include:"
		for supply in self.supplies:
			if supply.available:
				toPrint+=supply.name
				toPrint+="\n"
		print(toPrint)
		return(toPrint)
