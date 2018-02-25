from jsonclass import JSONClass
class Person(JSONClass):
    def __init__(self, name, title, skills):
        super().__init__()
        self.name=name
        self.title=title
        self.role=None
        self.task=None
        self.skills=[]

    def __str__(self):
        toReturn=self.name+" is a "+str(self.title)+"\n"
        if(self.role):
            toReturn+="Role: "+self.role
        else:
            toReturn+="Role: not yet assigned"
        toReturn+="\n"
        if(self.task):
          toReturn+="Working on "+str(self.task)
        else:
          toReturn+="No task assigned"
        return toReturn

    def assignRole(self, role):
        self.role=role

    def assignTask(self, task):
        self.task=task

    def getStatus(self):
        pass

class RN(Person):
    def __init__(self, name):
        self.skills=[]
        self.title="RN"
        super().__init__(name, self.title, self.skills)

class RT(Person):
    def __init__(self, name):
        self.skills=[]
        self.title="RT"
        super().__init__(name, self.title, self.skills)

class NP(Person):
    def __init__(self, name):
        skills=[]
        self.title="NP"
        super().__init__(name, self.title, self.skills)

class medStudent(Person):
    def __init__(self, name):
        skills=["observe"]
        self.title="medical student"
        super().__init__(name, self.title, self.skills)

class Staff(JSONClass):
    def __init__(self, people):
        super().__init__()
        self.staff=people

    def toJSON(self):
        toReturn=[]
        for person in self.staff:
            toReturn.append(person.toJSON())
        return toReturn