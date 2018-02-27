import json
import sys
from preemie_ppv import *
import tests
import pdb

b=PreemiePPVScenario()
b.loadData()

b.prepWarmer()
b.resuscitation()