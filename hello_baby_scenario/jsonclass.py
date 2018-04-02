import types
from collections import defaultdict
#This class needs some serious testing to troubleshoot it!

def simple_tree(): return defaultdict(simple_tree)

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

class JSONClass:
    def __init__(self):
        self.jsonList=[]

    def toJSON(self):
        toReturn={}
        for name in self.__dict__.keys():
            value=getattr(self, name)
            if isinstance(value, JSONClass):
                toReturn[name]=value.toJSON()
            else:
                toReturn[name]=self.recToJSON(value)
        return toReturn

    def recToJSON(self, item):
        toReturn=None
        if isinstance(item, dict):
            toReturn={}
            for key,value in item.items():
                toReturn[key]=self.recToJSON(value)
        elif isinstance(item, list):
            toReturn=[]
            for value in item:
                toReturn.append(self.recToJSON(value))
        elif (isinstance(item, types.MethodType) or isinstance(item, types.LambdaType)):
            toReturn=item.__name__
        elif isinstance(item, JSONClass):
            toReturn=item.toJSON()
        else:
            toReturn=item
        return toReturn

    def setJSON(self, jsonModel):
        for key,value in jsonModel.items():
            if key in self.__dict__.keys():
                if isinstance(self.__dict__[key], JSONClass):
                    self.__dict__[key].setJSON(value)
                else:
                    self.__dict__[key]=self.recSetJSON(self.__dict__[key], value)

    def recSetJSON(self, oldValue, jsonValue):
        toReturn=None
        if isinstance(oldValue, dict):
            toReturn={}
            for key,value in jsonValue.items():
                toReturn[key]=self.recToJSON(value)
            return toReturn
        elif isinstance(oldValue, list):
            toReturn=[]
            for value,i in enumerate(oldValue, start=1):
                toReturn[i]=self.recTOJSON(value)
        elif isinstance(oldValue, JSONClass):
            toReturn=oldValue
            oldValue.setJSON(jsonValue)
        else:
            toReturn=jsonValue
        return toReturn
