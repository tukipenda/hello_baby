from jsonclass import *

class SupplyUnvailableError(Exception):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

class Supply(JSONClass):
    def __init__(self, name):
        self.name=name
        self.available=False
        self.using=False

    def getSupply(self):
        self.available=True

    def placeSupply(self):
        self.using=True

    def __str__(self):
        return self.name

#need to adjust this class so that you have to fetch the maskType at the beginning
class BagMask(Supply):
    def __init__(self, masktype):
        super().__init__("mask")
        self.masktype=masktype
        self.PIP=0
        self.PEEP=0
        self.POP=0
        self.cmdDict={'setP': self.setPressuresString}

    def __str__(self):
        toReturn=""
        if self.masktype:
            toReturn="A "+self.masktype+" mask is available at bedside\n"
            toReturn+="PIP: "+str(self.PIP)+ " PEEP: "+str(self.PEEP)+" Pop-off Pressure: "+str(self.POP)
        else:
            toReturn="No mask is present at bedside"
        return toReturn

    def setPressures(self, PIP, PEEP, POP):
        if PIP:
            self.PIP=PIP
        if PEEP:
            self.PEEP=PEEP
        if POP:
            self.POP=POP

    def setPressuresString(self):
        PIP=input("Enter PIP: ")
        PEEP=input("Enter PEEP: ")
        POP=input("Enter POP: ")
        self.setPressures(PIP, PEEP, POP)

class ETT(Supply):
    def __init__(self, size):
        super().__init__("ETT")
        self.size=size

    def __str__(self):
        return (self.name+" size: "+self.size)

class Laryngoscope(Supply):
    def __init__(self, size):
        super().__init__("laryngoscope")
        self.size=size

    def __str__(self):
        return (self.name+" size: "+self.size)

class SupplyManager(JSONClass):
    def __init__(self, supplies):
        self.supplies=supplies
        self.availableSupplies={}

        #supplies that have been used for baby
        self.activeSupplies=[]

        self.cmdDict={"printSupplyList":(lambda :print([str(supply) for supply in self.supplies.values()])),
        "printAvailableSupplies":(lambda :print([str(supply) for supply in self.availableSupplies.values()]))}


    def fetchSupply(self, name, **kwargs):
        supply=self.getSupply(name, **kwargs)
        if supply:
            if not supply in self.availableSupplies.values():
                self.availableSupplies.append(supply)
                supply.getSupply()
        else:
            print("error")

    def placeSupply(self, name, **kwargs):
        supply=self.getSupply(name, **kwargs)
        if supply:
            if (supply in self.availableSupplies) and (not supply in self.activeSupplies):
                self.activeSupplies.append(supply)
                supply.placeSupply()
        else:
            print("error")


    #this method sucks
    def getSupply(self, name, **kwargs):
        toReturn=None
        for supply in self.supplies:
            gotSupply=True
            if supply.name!=name:
                gotSupply=False
            for key,value in kwargs.items():
                if hasattr(supply, key):
                    if getattr(supply, key)!=value:
                        gotSupply=False
            if gotSupply:
                toReturn=supply
        return toReturn

    def getMasks(self):
        toReturn=[]
        for supply in self.supplies:
            if supply.name=="mask":
                toReturn.append(supply)
        return toReturn