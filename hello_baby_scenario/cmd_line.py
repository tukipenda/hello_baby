import json
import sys
from scenario import Scenario
import tests

t=tests.Testing()
t.runTests()


#initializing scenario
b=Scenario()
b.loadData()


b.prepWarmer()
b.resuscitation()
b.scoring()