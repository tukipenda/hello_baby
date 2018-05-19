import models
from models import db
from app import app
import preemie_ppv_data as data
import time

baby_id=4
skin=models.PESkin.query.filter_by(baby_id=baby_id).first()

t=0
while(True):
    time.sleep(1)
    print(t)
    t+=1
    print(skin.is_dry)