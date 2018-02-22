from jsonclass import *

# temperature (turned on), suction, bag/mask, oxygen flow, baby timer
# supplies - ETT (sizes), masks, pulse ox, laryngoscope, hat, blankets, bulb suction, deep suction/meconium aspirator, preemie supplies

class SupplyUnvailableError(Exception):
	def __init__(self, expr, msg):
		self.expr = expr
		self.msg = msg

class Supply(JSONClass):
	def __init__(self, name):
		self.name=name
		self.using=False
		self.available=False

	def getSupply(self):
		self.available=True

	def useSupply(self):
		self.using=True

	def __str__(self):
		return self.name

class BagMask(Supply):
	def __init__(self, masktype=None):
		super().__init__("Bag Mask")
		self.masktype=masktype
		self.PIP=0
		self.PEEP=0
		self.POP=0
		self.cmdDict={'setP': self.setPressuresString, 'setMask': self.setMaskType}

	def __str__(self):
		toReturn=""
		if self.masktype:
			toReturn="A "+self.masktype+" mask is available at bedside\n"
			toReturn+="PIP: "+str(self.PIP)+ " PEEP: "+str(self.PEEP)+" Pop-off Pressure: "+str(self.POP)
		else:
			toReturn="No mask is present at bedside"
		return toReturn

	def setPressures(self, PIP, PEEP, POP):
		if self.masktype:
			if PIP:
				self.PIP=PIP
			if PEEP:
				self.PEEP=PEEP
			if POP:
				self.POP=POP
		else:
			raise SupplyUnvailableError("", "There is no mask present")
		 
	
	def setPressuresString(self):
		PIP=input("Enter PIP: ")
		PEEP=input("Enter PEEP: ")
		POP=input("Enter POP: ")
		self.setPressures(PIP, PEEP, POP)

	def setMaskType(self, masktype):
		self.masktype=masktype
		self.available=True

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
		self.setOxygen(flow, FIO2)

	def setSuction(self, suction):
		self.suction=suction
	
	def setTempMode(self, tempMode):
		self.tempMode=tempMode
	
	def getSupply(self, name):
		success=False
		for supply in self.supplies:
			if supply.name==name:
				supply.available=True
				success=True
		if not success:
			print(name+" is unavailable.")
			
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
