from flask import Flask, render_template, request, session
#from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

dirname=os.path.dirname(os.path.abspath(__file__))
dbpath='sqlite:///{0}/hello_baby.db'.format(dirname)

app = Flask(__name__, static_url_path='/static', template_folder="{0}/../templates/".format(dirname))
app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

#not secure
app.secret_key="something very easy"
app.debug=True

#toolbar = DebugToolbarExtension(app)

