from flask import Flask , request , render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

import os
if os.path.exists('data.db'):
   os.remove('data.db')

# Configure the app
app = Flask("db-app")

# Connect to SQL db
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite://///Users/mikeywilson/coding/courses/cs50/project/data.db'
db = SQLAlchemy(app)

class record(db.Model):
    name = db.Column(db.Text)
    age = db.Column(db.Integer)
    city = db.Column(db.Text)
    id = db.Column(db.Integer , primary_key=True)


    def __init__(self,n,a,c):
        self.name = n
        self.age = a
        self.city = c


@app.route("/index")
def myform():
    data = render_template("index.html")
    return data


@app.route("/add_data_sqlite")
def add_data_sqlite():
    n = request.args.get("name")
    a = request.args.get("age")
    c = request.args.get("city")
    
    db.create_all()
    obj = record(n ,a ,c)
    db.session.add(obj)
    db.session.commit()
    return "successfull"
