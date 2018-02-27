from scenario import *
from preemie_ppv import *

testing=PreemiePPVScenario()

#initializing scenario
testing.loadData()
testing.loadBabyUpdate()

#test updateTemp
class Testing:
    def __init__(self):
        self.scenario=testing

    def runTests(self):
        self.testPlaceSupply()
        self.testUpdateTemp()

    # test updateTemp
    def testUpdateTemp(self):
        pass

  # test placeSupply
    def testPlaceSupply(self):
        pass