from scenario import Scenario

testing=Scenario()
testing.loadData()

#test updateTemp
class Testing:
  def __init__(self):
    self.scenario=testing
 
  def runTests(self):
    self.testPlaceSupply()
 
  # test updateTemp
  
  # test placeSupply
  def testPlaceSupply(self):
    mgr=self.scenario.taskMGR
    fetch=mgr.taskList['fetch']
    place=mgr.taskList['place']
    fetch.complete("pulse_ox")
    place.complete("pulse_ox")
    place.complete("ETT")
    print(self.scenario.baby.supplies)