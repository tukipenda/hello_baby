import os
dirname=os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(dirname+"/hello_baby_scenario/")
from app import app, db
from models import *
from views import *
app.logger.info("Here")

if __name__ == '__main__':
    app.run()