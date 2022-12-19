from flask import Flask , request , render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy

import os
if os.path.exists('data.db'):
   os.remove('data.db')

# Configure the app
app = Flask(__name__)

# Connect to SQL db
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite://///Users/mikeywilson/coding/courses/cs50/project/data.db'
db = SQLAlchemy(app)

# Create SQL database and table
class record(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    type = db.Column(db.Text)
    make = db.Column(db.Text)
    model = db.Column(db.Text)
    serial = db.Column(db.Integer)
    date = db.Column(db.Text)
    value = db.Column(db.Integer)

    def __init__(self,t,m,o,s,d,v):
        self.type = t
        self.make = m
        self.model = o
        self.serial = s
        self.date = d
        self.value = v


@app.route("/")
def myform():
    data = render_template("index.html")
    return data

# Add user from html form into SQL database
@app.route("/add_data")
def add_data():
    t = request.args.get("type")
    m = request.args.get("make")
    o = request.args.get("model")
    s = request.args.get("serial")
    d = request.args.get("date")
    v = request.args.get("value")
    
    db.create_all()
    obj = record(t,m,o,s,d,v)
    db.session.add(obj)
    db.session.commit()
    # Display SQL data in html form
    records = record.query.all()
    return render_template('index.html', records=records)

# Delete row from SQL database table
@app.route("/delete_data<int:id>")
def delete_data(id):
    row = record.query.get_or_404(id)
    try:
        db.session.delete(row)
        db.session.commit()
        # Display SQL data in html form
        records = record.query.all()
        return render_template('index.html', records=records)

    except:
        records = record.query.all()
        return render_template('index.html', records=records)