from flask import Flask, request, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# Configure the app
app = Flask(__name__)
app.secret_key = "kjsgdkjgsdlkhjflgjdslnaksnkaf"

# Connect to SQL db
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///data.db'
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
        total = db.session.query(func.sum(record.value)).filter().scalar()
        if total is None:
            total = 0
        return render_template('gear.html', records=records, total=total)
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
        total = db.session.query(func.sum(record.value)).filter().scalar()
        if total is None:
            total = 0
        flash("gear successfully deleted!")
        return render_template('gear.html', records=records, total=total)
    except:
        records = record.query.all()
        flash("error: unable to delete")
        return render_template('gear.html', records=records, total=total)
