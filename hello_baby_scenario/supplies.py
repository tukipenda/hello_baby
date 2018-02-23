from jsonclass import *

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
    
class Supplies(JSONClass):
  def __init__(self):
    self.supplies=[]
  