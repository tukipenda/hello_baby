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
        self.pp=" ".join(name.split("_")).title()

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
    def __init__(self, size):
        super().__init__("mask")
        self.size=size
        self.using=False
        self.pp=self.size+" "+self.pp

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return ((self.name == other.name) and (self.size==other.size))
        return False

class ETT(Supply):
    def __init__(self, size):
        super().__init__("ETT")
        self.size=size
        self.pp="ETT "+str(self.size)

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
        self.pp=self.pp+" "+str(self.size)

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

    def useMask(self, masktype):
        for mask in self.supplies['mask']:
            if mask.size==masktype:
                mask.using=True
            else:
                mask.using=False

    def fetchSupply(self, name, size=None):
        supply=self.getSupply(name, size=size)
        if supply:
            supply.available=True

    #can't use this with ETT, laryngoscope, mask
    def placeSupply(self, name, size=None):
        supply=self.getSupply(name, size=size)
        if supply:
            supply.placed=True

    def getSupply(self, name, size=None):
        if name in ["ETT", "mask", "laryngoscope"]:
            if size:
                className=name[0].upper()+name[1:]
                supplyClass=getattr(sys.modules[__name__], className)
                testSupply=supplyClass(size)
                for supply in self.supplies[name]:
                    if supply==testSupply:
                        return supply
            else:
                return None
        else:
            if name in self.supplies.keys():
                return self.supplies[name]
        return None