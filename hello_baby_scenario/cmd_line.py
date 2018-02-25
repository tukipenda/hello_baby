import json
import sys
from scenario import Scenario
import tests

t=tests.Testing()
t.runTests()


#initializing scenario
babyScenario=Scenario()
babyScenario.loadData()


babyScenario.prepWarmer()
babyScenario.resuscitation()
babyScenario.scoring()