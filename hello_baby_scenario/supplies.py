from jsonclass import *
import sys

class SupplyUnvailableError(Exception):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

class Supply(JSONClass):
    def __init__(self, name):
        self.name=name
        self.available=False
        self.placed=False

    def getSupply(self):
        self.available=True

    def placeSupply(self):
        self.using=True

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.name == other.name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class Mask(Supply):
    def __init__(self, masktype):
        super().__init__("mask")
        self.masktype=masktype
        self.using=False
        self.PIP=0
        self.PEEP=0
        self.POP=0

    def setPressures(self, PIP, PEEP, POP):
        if PIP:
            self.PIP=PIP
        if PEEP:
            self.PEEP=PEEP
        if POP:
            self.POP=POP

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return ((self.name == other.name) and (self.masktype==other.masktype))
        return False

class ETT(Supply):
    def __init__(self, size):
        super().__init__("ETT")
        self.size=size

    def __str__(self):
        return (self.name+" size: "+str(self.size))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return ((self.name == other.name) and (self.size==other.size))
        return False


class Laryngoscope(Supply):
    def __init__(self, size):
        super().__init__("laryngoscope")
        self.size=size

    def __str__(self):
        return (self.name+" size: "+str(self.size))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return ((self.name == other.name) and (self.size==other.size))
        return False

class SupplyManager(JSONClass):
    def __init__(self, supplies):
        self.supplies=supplies
        self.supplyList=[] #I think this is a bad hack for getting things to work.  Need a better solution!
        for name in self.supplies.keys():
            if name in ["ETT", "laryngoscope", "mask"]:
                self.supplyList.extend(self.supplies[name])
            else:
                self.supplyList.append(self.supplies[name])

    def fetchSupply(self, name, *args):
        supply=self.getSupply(name, *args)
        if supply:
            supply.available=True

    #can't use this with ETT, laryngoscope, mask
    def placeSupply(self, name, *args):
        supply=self.getSupply(name, *args)
        if (supply and supply.available):
            supply.placed=True
        else:
            print("error") #god this needs to be better

    def getSupply(self, name, *args):
        if name in ["ETT", "laryngoscope", "mask"]:
            className=name[0].upper()+name[1:]
            supplyClass=getattr(sys.modules[__name__], className)
            testSupply=supplyClass(*args)
            for supply in self.supplies[name]:
                if supply==testSupply:
                    return supply
        else:
            if name in self.supplies.keys():
                return self.supplies[name]
        return None