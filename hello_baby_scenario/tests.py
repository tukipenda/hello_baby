from scenario import Scenario

testing=Scenario()
testing.loadData()

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
    mgr=self.scenario.taskMGR
    fetch=mgr.taskList['fetch']
    place=mgr.taskList['place']
    fetch.complete("pulse_ox")
    place.complete("pulse_ox")
    place.complete("ETT")