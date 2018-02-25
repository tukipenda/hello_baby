import json
import sys
from scenario import Scenario
import tests
import pdb

t=tests.Testing()
t.runTests()


#initializing scenario
b=Scenario()
b.loadData()
pdb.set_trace()
print(b.supplyMGR.getSupply("ETT", '2.5'))


b.prepWarmer()
b.resuscitation()
b.scoring()