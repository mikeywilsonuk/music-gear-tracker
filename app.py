from flask import Flask , request , render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy

import os
if os.path.exists('data.db'):
   os.remove('data.db')

# Configure the app
app = Flask(__name__)
app.secret_key = "kjsgdkjgsdlkhjflgjdslnaksnkaf"

# Connect to SQL db
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite://///Users/mikeywilson/coding/courses/cs50/project/data.db'
db = SQLAlchemy(app)

# Create SQL database and table
class record(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    type = db.Column(db.Text)
    manufacturer = db.Column(db.Text)
    model = db.Column(db.Text)
    serial = db.Column(db.Integer)
    date = db.Column(db.Text)
    value = db.Column(db.Integer)

    def __init__(self,t,m,o,s,d,v):
        self.type = t
        self.manufacturer = m
        self.model = o
        self.serial = s
        self.date = d
        self.value = v


# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gear")
def gear():
    try:
        records = record.query.all()
        # totval = record.query.value()
        # for totval in record:
        return render_template('gear.html', records=records)
    except:
        return render_template('gear.html')

@app.route("/about")
def about():
    return render_template("about.html")

# Add user from html form into SQL database
@app.route("/add_data", methods=["POST"])
def add_data():
    try:
        t = request.form.get("type")
        m = request.form.get("manufacturer")
        o = request.form.get("model")
        s = request.form.get("serial")
        d = request.form.get("date")
        v = request.form.get("value")
        
        db.create_all()
        obj = record(t,m,o,s,d,v)
        db.session.add(obj)
        db.session.commit()
        # Display SQL data in html form
        flash("gear successfully registered!")
        return render_template("index.html")
    except:
        flash("error: unable to register")
        return render_template("index.html")


# Delete row from SQL database table
@app.route("/delete_data<int:id>")
def delete_data(id):
    row = record.query.get_or_404(id)
    try:
        db.session.delete(row)
        db.session.commit()
        # Display SQL data in html form
        records = record.query.all()
        flash("gear successfully deleted!")
        return render_template('gear.html', records=records)

    except:
        records = record.query.all()
        flash("error: unable to delete")
        return render_template('gear.html', records=records)

# # Ensure responses aren't cached
# @app.after_request
# def after_request(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response