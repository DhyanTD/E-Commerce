import re
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
import os
from sqlalchemy import exists
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect
import base64

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

# Table Customer


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

# Table Cart


class Cart(db.Model):
    CART_ID = db.Column(db.Integer, primary_key=True)
    CUST_ID = db.Column(db.Integer, ForeignKey(
        Customer.CUST_ID), nullable=False)

# Table Seller


class Seller(db.Model):
    S_ID = db.Column(db.Integer, primary_key=True)
    F_NAME = db.Column(db.String, nullable=False)
    L_NAME = db.Column(db.String, nullable=False)
    S_ADDRESS = db.Column(db.String, nullable=False)
    PH_NO = db.Column(db.Integer, nullable=False)
    E_MAIL = db.Column(db.String, nullable=False)
    GENDER = db.Column(db.String, nullable=False)
    USERNAME = db.Column(db.String, unique=True, nullable=False)
    PASSWORD = db.Column(db.String, nullable=False)

# Table Category


class Category(db.Model):
    C_ID = db.Column(db.Integer, primary_key=True)
    C_NAME = db.Column(db.String, nullable=False)

# Table Products


class Products(db.Model):
    P_ID = db.Column(db.Integer, primary_key=True)
    P_NAME = db.Column(db.String, nullable=False)
    COST = db.Column(db.Float, nullable=False)
    COUNT = db.Column(db.Integer, nullable=False)
    S_ID = db.Column(db.Integer, ForeignKey(Seller.S_ID), nullable=False)
    C_ID = db.Column(db.Integer, ForeignKey(Category.C_ID), nullable=False)
    P_IMG = db.Column(db.Text, nullable=False)
    P_DESC = db.Column(db.String, nullable=False)

    # def __repr__(self) -> str:
    #     return f"{self.P_NAME} - {self.COUNT} - {self.COST} - {self.P_DESC} - {self.P_IMG}"
    def __repr__(self):
        return '<Products %r>' % (self.P_NAME)

# Table Transaction


class Transaction(db.Model):
    T_ID = db.Column(db.Integer, primary_key=True)
    AMMOUNT = db.Column(db.Float, nullable=False)
    STATUS = db.Column(db.String, nullable=False)
    P_ID = db.Column(db.Integer, ForeignKey(Products.P_ID), nullable=False)
    CUST_ID = db.Column(db.Integer, ForeignKey(
        Customer.CUST_ID), nullable=False)

# Table Product_delivery


class Product_delivery(db.Model):
    DEL_ID = db.Column(db.Integer, primary_key=True)
    DEL_ADDRESS = db.Column(db.String, nullable=False)
    P_ID = db.Column(db.Integer, ForeignKey(Products.P_ID), nullable=False)
    S_ID = db.Column(db.Integer, ForeignKey(Seller.S_ID), nullable=False)
    CUST_ID = db.Column(db.Integer, ForeignKey(
        Customer.CUST_ID), nullable=False)

# Table Cart_products


class Cart_products(db.Model):
    CP_ID = db.Column(db.Integer, primary_key=True)
    CART_ID = db.Column(db.Integer, ForeignKey(Cart.CART_ID), nullable=False)
    P_ID = db.Column(db.Integer, ForeignKey(Products.P_ID), nullable=False)

# Table Orders


class Orders(db.Model):
    O_ID = db.Column(db.Integer, primary_key=True)
    CUST_ID = db.Column(db.Integer, ForeignKey(
        Customer.CUST_ID), nullable=False)
    S_ID = db.Column(db.Integer, ForeignKey(Seller.S_ID), nullable=False)
    P_ID = db.Column(db.Integer, ForeignKey(Products.P_ID), nullable=False)
    STATE = db.Column(db.String, nullable=False)
    DISTRICT = db.Column(db.String, nullable=False)
    CITY = db.Column(db.String, nullable=False)
    STREET = db.Column(db.String, nullable=False)
    PINCODE = db.Column(db.Integer, nullable=False)
    DATE = db.Column(db.String, nullable=False)

# home page


@app.route("/")
def home():
    prdts = db.session.query(Products.P_NAME,Products.COUNT,Products.COST,Products.P_IMG,Products.P_DESC).all()
    return render_template('c_index.html',products=prdts)

# customer login page


@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        exists = db.session.query(Customer.USERNAME).filter_by(
            USERNAME=uname, PASSWORD=psw).first() is not None
        if(exists):
            params["crnt_usr"] = uname
            session['cust_login'] = True
            return redirect('/')
        else:
            return redirect('/signup')
    return render_template('login.html')

# customer signup page


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
            print
            redirect("/signup")
    return render_template('signup.html')

# seller login page


@app.route("/s_login", methods=["GET", "POST"])
def s_login():
    if(request.method == "POST"):
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        exists = db.session.query(Seller.USERNAME).filter_by(
            USERNAME=uname, PASSWORD=psw).first() is not None
        if(exists):
            params["crnt_s_usr"] = uname
            session['sell_login'] = True
            return redirect('/seller_index')
        else:
            return redirect('/s_signup')
    return render_template('s_login.html')

# seller signup page


@app.route("/s_signup", methods=["GET", "POST"])
def s_signup():
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
            entry = Seller(F_NAME=fname, L_NAME=lname, S_ADDRESS=address, PH_NO=phno,
                           E_MAIL=email, GENDER=gender, USERNAME=uname, PASSWORD=psw)
            db.session.add(entry)
            db.session.commit()
            return redirect("/seller_index")
        except:
            redirect("/s_signup")
    return render_template('s_signup.html')

# payment page
# @app.route('/payment', methods=["GET","POST"])
# def payment():
#     if(request.method=="POST"):

#     return render_template('payment.html')


@app.route("/seller_index", methods=["GET", "POST"])
def seller_index():
    return render_template("seller_index.html")


@app.route("/s_addprdts", methods=["GET", "POST"])
def s_addprdts():
    if(request.method == "POST" and params["crnt_s_usr"]!=""):
        try:
            category = request.form.get("category")
            p_name = request.form.get("p_name")
            desc = request.form.get("desc")
            count = request.form.get("count")
            cost = request.form.get("cost")
            img = request.form.get("psw")
            f = request.files["psw"]
            f.save('C:\\Users\jeev\Downloads\E-Commerce-main (1)\E-Commerce-main\static\\assets\images\\'+f.filename)
            c_id = db.session.query(Category.C_ID).filter_by(
                C_NAME=category).first()
            s_id = db.session.query(Seller.S_ID).filter_by(
                USERNAME=params['crnt_s_usr']).first()
            img = str.encode(f.filename)
            entry = Products(P_NAME=p_name, COST=cost, COUNT=count,
                             S_ID=s_id[0], C_ID=c_id[0], P_IMG=img, P_DESC=desc)
            db.session.add(entry)
            db.session.commit()
            return redirect("/seller_index")
        except:
            return redirect("/s_addprdts")
    return render_template("s_addprdts.html")

@app.route("/your_products", methods=["GET" , "POST"])
def your_products():
    if(request.method == "GET"):
        try:
            s_id = db.session.query(Seller.S_ID).filter_by(
                USERNAME=params['crnt_s_usr']).all()
            # s_id = s_id[0]
            # print(s_id[0][0])
            prdcts = db.session.query(Products.P_NAME,Products.COUNT,Products.COST,Products.P_DESC).filter_by(S_ID = s_id[0][0]).all()
            # print(prdcts)
            return render_template("your_products.html", prdcts=prdcts)
        except:
            return redirect("/s_logged_out")

@app.route('/displayprdts')
def display():
    if(request.method == "GET"):
        prdts = db.session.query(Products).all()
        return render_template('displayprdts.html',products=prdts)
    return render_template('displayprdts.html')


@app.route("/404")
def not_found():
    return render_template("404.html")

@app.route("/s_logged_out")
def loggedout():
    return render_template("s_logged_out.html")

@app.route('/logout')
def logout():
    session['cust_login'] = False
    return render_template('login.html')

app.run(debug=True)
