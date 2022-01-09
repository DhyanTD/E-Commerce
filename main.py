import re
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
import os
from sqlalchemy import exists
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
db = SQLAlchemy(app)


class Customer(db.Model):
    CUST_ID = db.Column(db.Integer, primary_key=True)
    F_NAME = db.Column(db.String(10), nullable=False)
    L_NAME = db.Column(db.String(10), nullable=False)
    ADDRESS = db.Column(db.String(120), nullable=False)
    PH_NO = db.Column(db.Integer, nullable=False)
    E_MAIL = db.Column(db.String(30), nullable=False)
    GENDER = db.Column(db.String(10), nullable=False)
    USERNAME = db.Column(db.String(20), unique=True, nullable=False)
    PASSWORD = db.Column(db.String(8), nullable=False)


class Cart(db.Model):
    CART_ID = db.Column(db.Integer, primary_key=True)
    CUST_ID = db.Column(db.Integer, ForeignKey(
        Customer.CUST_ID), nullable=False)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        exists = db.session.query(Customer.USERNAME).filter_by(
            USERNAME=uname, PASSWORD=psw).first() is not None
        if(exists):
            params["crnt_usr"] = uname
            return redirect('/')
        else:
            return redirect('/signup')
    return render_template('login.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if(request.method == "POST"):
        try:
            fname = request.form.get("Fname")
            lname = request.form.get("Lname")
            email = request.form.get("email")
            phno = request.form.get("phno")
            gender = request.form.get("gender")
            address = request.form.get("address")
            uname = request.form.get("username")
            psw = request.form.get("psw")
            entry = Customer(F_NAME=fname, L_NAME=lname, ADDRESS=address, PH_NO=phno,
                             E_MAIL=email, GENDER=gender, USERNAME=uname, PASSWORD=psw)
            db.session.add(entry)
            data = db.session.query(Customer.CUST_ID).filter_by(
                USERNAME=uname).first()
            db.session.flush()
            entry1 = Cart(CUST_ID=data[0])
            db.session.add(entry1)
            db.session.commit()
            return redirect("/")
        except:
            redirect("/signup")
    return render_template('signup.html')

app.run(debug=True)
