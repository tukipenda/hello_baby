from flask import Flask, render_template, request, session
#from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__, static_url_path='/static')
dirname=os.path.dirname(os.path.abspath(__file__))
dbpath='sqlite:///{0}/hello_baby.db'.format(dirname)
app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

#admin = User.query.filter_by(username='admin').first()
#if not admin:
#    admin = User(username='admin')
 #   db.session.add(admin)
  #  db.session.commit()
#db.session.add(scenario)
#db.session.commit()
#createBaby(admin, scenario)
#db.session.commit()

#not secure
app.secret_key="something very easy"
app.debug=True

#toolbar = DebugToolbarExtension(app)

