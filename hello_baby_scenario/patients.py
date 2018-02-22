from jsonclass import JSONClass

#need a better way to get and set vitals, parts of PE!


#update temp - depends on heat, drying, time, GA, transwarmer
#update cardiac - depends on respiratory status, temp, infant's clinical status
#update respiratory status - depends on temp, time, suctioning, stim, PPV, intubation, FiO2
#tone/cry - depends on temp, neuro, cardiac, respiratory status
#O2 sat - depends on respiratory status, time, FiO2
# bp - depends on what?
#secretions - depends on suctioning, respiration, scenario, intubation, deep suctioning

# skin, abdomen, other - fixed

#scenarios - term with MAS, very preterm with RDS, term with TTN

class Baby(JSONClass):
	def __init__(self, ga, nc):
		super().__init__()
		self.ga=ga
		self.nc=nc
		self.vitals=None
		self.PE=None
		self.delivered=False
		self.cmdDict={'getPE':self.getPE, 'getVitals':self.getVitals}

	def complications(self):
		if len(self.nc)==0:
			return "no prenatal complications"
		else:
			return self.nc

	def initialize(self, vs, PE):
		self.vitals=vs
		self.PE=PE

	def deliverBaby(self):
		self.delivered=True

	def getPE(self):
		toPrint=""
		for key in self.PE.keys():
			toPrint+=key+": "
			for k in self.PE[key].keys():
				toPrint+=k+"-"+str(self.PE[key][k])+" "
			toPrint+=("\n\n")
		print(toPrint)

	def getVitals(self):
		for key in self.vitals.keys():
			print(key+": "+str(self.vitals[key]))

	def __str__(self):
		description="The baby is "+str(self.ga)+" weeks old with "+self.complications()+"."
		return description

#would like to refactor below to a dict without using the classes
#Also would like to separate the presentation of the data from the data a little more
class momInfo(JSONClass):
    def getText(self):
        pass

class prenatalLabs(momInfo):
  def __init__(self, vzv, rubella, HIV, hepB, RPR, GC, chlamydia):
	  self.labs={"RPR":RPR, "rubella":rubella, "HIV":HIV, "hepB": hepB, "vzv":vzv, "GC":GC, "chlamydia": chlamydia}
	  self.printName="Prenatal Labs"
	  self.text=self.getText()

  def getText(self):
    toReturn="Prenatal labs: "
    for lab,value in self.labs.items():
      toReturn+=str(value)+" "
    return toReturn

class HSVStatus(momInfo):
  def __init__(self, HSV, lesions, acyclovir):
	  self.HSV=HSV
	  self.lesions=lesions
	  self.acyclovir=acyclovir
	  self.printName="HSV Status"
	  self.text=self.getText()

  def getText(self):
	  toReturn=""
	  if not self.HSV:
	    toReturn="Mom is negative for HSV."
	  else:
	      toReturn="Mom is positive for HSV."
	      if self.lesions:
	          toReturn+=" Active lesions are present."
	      if self.acyclovir:
	          toReturn+=" Mom is taking acyclovir."
	  return toReturn

class GBSStatus(momInfo):
  def __init__(self, GBS, fever, antibiotics, moreThanFour):
	  self.GBS=GBS
	  self.fever=fever
	  self.antibiotics=antibiotics
	  self.moreThanFour=moreThanFour
	  self.printName="GBS Status"
	  self.text=self.getText()

  def getText(self):
    toReturn=""
    if not self.GBS:
      toReturn+="Mom is GBS negative."
    else:
      toReturn+="Mom is GBS positive."
    if self.fever!=None:
      toReturn+=" She was febrile to "+str(self.fever)
    if len(self.antibiotics)>0:
      toReturn+=" She took to the following antibiotics: "
      for i,a in enumerate(self.antibiotics):
        if i>1:
            toReturn+=", "
        toReturn+=a
      if self.moreThanFour:
          toReturn+=" She received antibiotics more than four hours ahead of delivery."
      else:
          toReturn+=" Antibiotic prophylaxis was inadequate."
    return toReturn

class ROM(momInfo):
  def __init__(self, ROM, clear):
    self.ROM=ROM
    self.clear=clear
    self.printName="ROM"
    self.text=self.getText()

  def getText(self):
    toReturn=""
    if self.ROM>0:
        toReturn="ROM occurred "+str(self.ROM)+" hours prior to delivery. "
    else:
        toReturn="ROM occurred at time of delivery. "
    if self.clear:
        toReturn+="Fluids were clear."
    return toReturn


class GP(momInfo):
	def __init__(self, gestation, parity, term, preterm, abortion, living, parityCurrent):
		self.gestation=gestation
		self.parity=parity
		self.term=term
		self.preterm=preterm
		self.abortion=abortion
		self.living=living
		self.parityCurrent=parityCurrent
		self.text=self.getText()
		self.printName="GP"

	def getText(self):
		return ("G"+str(self.gestation)+"P"+str(self.parity))

class Mom(JSONClass):
	def __init__(self, momAge, prenatalLabs, HSVStatus, GBSStatus, momComplications, ROM, medications, GP):
		super().__init__()
		self.data=[prenatalLabs, HSVStatus, GBSStatus, ROM, GP]
		self.text="Mom is a "+str(momAge)+" year old "+str(GP)+" woman."


# Defining the delivery

class Delivery(JSONClass):
	def __init__(self, deliveryType, stat):
		self.dT=deliveryType
		self.stat=stat

	def __str__(self):
		statString="stat " if (self.stat==True) else ""
		return (statString+self.dT)

