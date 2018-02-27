import json
import sys
from preemie_ppv import *
import tests
import pdb



print("here")
b=PreemiePPVScenario()
b.loadData()

b.prepWarmer()
b.resuscitation()
