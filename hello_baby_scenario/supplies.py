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
    
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
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
        self.activeSupplies={}

        self.cmdDict={"printSupplyList":(lambda :print([str(supply) for supply in self.supplies.values()])),
        "printAvailableSupplies":(lambda :print([str(supply) for supply in self.availableSupplies.values()]))}


    def fetchSupply(self, name, **kwargs):
        supply=self.getSupply(name, **kwargs)
        if supply:
            supply.available=True
            self.addSupplyToList(self.availableSupplies, supply)

    def placeSupply(self, name, **kwargs):
        supply=self.getSupply(name, **kwargs)
        if (supply and supply.available):
            supply.using=True
            self.addSupplyToList(self.activeSupplies, supply)
        else:
            print("error") #god this needs to be better


    #this method sucks
    def getSupply(self, name, **kwargs):
        return self.getSupplyFromList(self.supplies, name, **kwargs)
   
    def getSupplyFromList(self, searchList, name, **kwargs):
        if name in searchList.keys():
            toCheck=self.supplies[name]
            if not isinstance(toCheck, list):
                toCheck=[toCheck]
            for supply in toCheck:
                gotSupply=True
                for key,value in kwargs.items():
                    if hasattr(supply, key):
                        if getattr(supply, key)!=value:
                            gotSupply=False
                if gotSupply:
                    return supply
        return None
   
    def addSupplyToList(self, addList, supply):
        if not supply.name in addList:
            addList[supply.name]=supply
        else:
            toCheck=addList[supply.name]
            if not isinstance(toCheck, list):
                toCheck=[toCheck]
            for checkSupply in toCheck:
                if checkSupply==supply:
                    return # don't add the supply as its already there
            toCheck.append(supply)
            addList[supply.name]=toCheck
