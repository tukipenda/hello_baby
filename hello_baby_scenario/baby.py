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
        self.supplies={}

    def initialize(self, vs, PE):
        self.vitals=vs
        self.PE=PE

    def deliver(self):
        self.delivered=True
    
    def has(supplyName):
        for supply in self.supplies:
            if suppy.name==supplyName:
                return True
        return False