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
    name = db.Column(db.Text)
    age = db.Column(db.Integer)
    city = db.Column(db.Text)
    id = db.Column(db.Integer , primary_key=True)

    def __init__(self,n,a,c):
        self.name = n
        self.age = a
        self.city = c


@app.route("/")
def myform():
    data = render_template("index.html")
    return data

# Add user from html form into SQL database
@app.route("/add_data_sqlite")
def add_data_sqlite():
    n = request.args.get("name")
    a = request.args.get("age")
    c = request.args.get("city")
    
    db.create_all()
    obj = record(n ,a ,c)
    db.session.add(obj)
    db.session.commit()
    # Display SQL data in html form
    records = record.query.all()
    return render_template('index.html', records=records)

# Delete row from SQL database table
@app.route("/delete_data_sqlite<int:id>")
def delete_data_sqlite(id):
    row = record.query.get_or_404(id)
    try:
        db.session.delete(row)
        db.session.commit()
        flash("Deleted Successfully")
        # Display SQL data in html form
        records = record.query.all()
        return render_template('index.html', records=records)

    except:
        records = record.query.all()
        return render_template('index.html', records=records)