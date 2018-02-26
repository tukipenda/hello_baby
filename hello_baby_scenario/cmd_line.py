import json
import sys
from preemie_ppv import *
import tests
import pdb

t=tests.Testing()
t.runTests()
b=PreemiePPVScenario()
b.loadData()


b.prepWarmer()
b.resuscitation()
b.scoring()