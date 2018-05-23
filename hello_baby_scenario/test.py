import models
from models import db
from app import app
import preemie_ppv_data as data
import time

baby_id=1
m=models.getExams(baby_id)
for key, value in m.items():
    print("{key}: {value}".format(key=key, value=value))