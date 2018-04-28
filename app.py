from flask import Flask, render_template, request, session
#from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/hello_baby.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
db.create_all()

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

