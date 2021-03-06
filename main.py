from dis import dis
import re
from tkinter import CASCADE
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
import os
from sqlalchemy import exists
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect
import datetime
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
    P_ID = db.Column(db.Integer, ForeignKey(Products.P_ID,ondelete=CASCADE,onupdate=CASCADE), nullable=False)

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
    PIN_CODE = db.Column(db.Integer, nullable=False)
    DATE = db.Column(db.String, default=datetime.datetime.utcnow, nullable=False)

# home page


@app.route("/")
def home():
    prdts = db.session.query(Products.P_ID, Products.P_NAME,Products.COUNT,Products.COST,Products.P_IMG,Products.P_DESC).all()
    return render_template('c_index.html',products=prdts)

# Help & Support
@app.route("/hc")
def hc():
    return render_template('hc.html')

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
            print(params['crnt_usr'])
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


@app.route("/seller_index", methods=["GET", "POST"])
def seller_index():
    return render_template("seller_index.html")

@app.route("/readmore")
def readmore():
    return render_template('readmore.html')


@app.route("/s_addprdts", methods=["GET", "POST"])
def s_addprdts():
    if  session['sell_login']:
        if(request.method == "POST"):
            try:
                category = request.form.get("category")
                p_name = request.form.get("p_name")
                desc = request.form.get("desc")
                count = request.form.get("count")
                cost = request.form.get("cost")
                img = request.form.get("psw")
                f = request.files["psw"]
                f.save('C:\\Users\\jeev\\OneDrive\\Documents\\GitHub\\E-Commerce\\static\\assets\\images\\'+f.filename)
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
                return redirect("/s_logged_out")
        return render_template("s_addprdts.html")
    return render_template("seller_index.html")

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

@app.route("/c_logged_out")
def c_loggedout():
    return render_template("c_logged_out.html")

@app.route('/logout')
def logout():
    session['cust_login'] = False
    return render_template('c_index.html')

@app.route("/s_logout")
def s_logout():
    session['sell_login'] = False
    return render_template("seller_index.html")

@app.route('/add/<int:p_id>')
def add(p_id):
    try:
        cust = db.session.query(Customer.CUST_ID).filter_by(USERNAME=params['crnt_usr']).all()
        cart = db.session.query(Cart.CART_ID).filter_by(CUST_ID=cust[0][0])
        entry = Cart_products(CART_ID=cart,P_ID=p_id)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
    except:
        return redirect('/c_logged_out')


@app.route('/deleteprdct/<string:p_id>')
def deleteprdct(p_id):
    s_id = db.session.query(Seller.S_ID).filter_by(
                USERNAME=params['crnt_s_usr']).all()
    prdcts = db.session.query(Products).filter_by(P_ID = p_id).all()
    print(p_id)
    print(prdcts)
    for p in prdcts:
        db.session.delete(p)
    db.session.commit()
    return redirect("/manage_prdcts")

@app.route('/manage_prdcts')
def manage():
    try:
        s_id = db.session.query(Seller.S_ID).filter_by(
                USERNAME=params['crnt_s_usr']).all()
        prdcts = db.session.query(Products).filter_by(S_ID = s_id[0][0]).all()
        return render_template('manage_prdcts.html',prdcts=prdcts)
    except:
        return redirect('/s_logged_out')
    
@app.route('/cart')
def cart():
    try:
        custid = db.session.query(Customer.CUST_ID).filter_by(USERNAME=params['crnt_usr']).all()
        cid = db.session.query(Cart.CART_ID).filter_by(CUST_ID=custid[0][0]).all()
        pid = []
        for p in db.session.query(Cart_products.P_ID).filter_by(CART_ID=cid[0][0]):
            print(p)
            pid.append(p[0])
        print(pid)
        # print(cid[0][0])
        # c = cid[0][0]
        prdcts = []
        # res = db.engine.execute(f"SELECT * FROM `Products` WHERE `Products`.`P_ID` IN (SELECT `Cart_products`.`P_ID` FROM `Cart_products` WHERE `Cart_products`.`CART_ID`={cid[0][0]}")
        for p in pid:
            prdcts.append(db.session.query(Products).filter_by(P_ID=p).all())
        print(prdcts)
        return render_template('c_cart.html',prdcts=prdcts)
    except:
        return redirect('/c_logged_out')

@app.route('/payment',methods=["GET" , "POST"])
def payment():
    if(request.method == "POST"):
        dist = request.form.get('district')
        state = request.form.get('state')
        city = request.form.get('city')
        pincode = request.form.get('zip')
        cust = db.session.query(Customer.CUST_ID).filter_by(USERNAME=params['crnt_usr']).all()
        cart = db.session.query(Cart.CART_ID).filter_by(CUST_ID=cust[0][0])
        pid = db.session.query(Cart_products.P_ID).filter_by(CART_ID=cart[0][0]).all()
        sid = db.session.query(Products.S_ID).filter_by(P_ID=pid[0][0])
        # prdct = db.session.query(Products).filter_by(P_ID=pid[0][0])
        entry = Orders(CUST_ID=cust[0][0],S_ID=sid[0][0],P_ID=pid[0][0],STATE=state,DISTRICT=dist,CITY=city,PIN_CODE=pincode)
        db.session.add(entry)
        db.session.commit()
        custid = db.session.query(Customer.CUST_ID).filter_by(USERNAME=params['crnt_usr']).all()
        cid = db.session.query(Cart.CART_ID).filter_by(CUST_ID=custid[0][0]).all()
        prdcts = db.session.query(Cart_products).filter_by(CART_ID=cid[0][0])
        for p in prdcts:
            db.session.delete(p)
        db.session.commit()
        return redirect('/c_po')
        # return render_template('payment.html',prdcts=prdct)
    return render_template('payment.html')

@app.route('/c_po')
def po():
    # custid = db.session.query(Customer.CUST_ID).filter_by(USERNAME=params['crnt_usr']).all()
    # cid = db.session.query(Cart.CART_ID).filter_by(CUST_ID=custid[0][0]).all()
    # pid = db.session.query(Cart_products.P_ID).filter_by(CART_ID=cid[0][0])
    # prdcts = db.session.query(Products).filter_by(P_ID=pid).filter_by(Products.COUNT<1).all()
    # for p in prdcts:
    #     db.session.delete(p)
    #     db.session.commit()
    return render_template('c_po.html')

app.run(debug=True)