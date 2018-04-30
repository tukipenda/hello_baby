import os
import sys
newpath=os.path.dirname(os.path.abspath(__file__))
sys.path.append(newpath+"/hello_baby_scenario/")
import models, views
from app import app

if __name__ == '__main__':
    app.run()