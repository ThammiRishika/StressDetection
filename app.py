import os
import smtplib
import random
import string
from datetime import datetime
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from database import db_connect, user_reg,viewpost1,viewcomment1,vaact,analysis1,analysis2,post_add,comment_add,adv_reg,admin_loginact,student_loginact,ins_loginact,view,send_msg,view_msg,view_std,c_search,requestact
from database import accept_act,reject_act,ins_profile,delete_act,std_profile,delete1_act,view_req,approve1_act,reject1_act,view_frd,add_adv,view_req1,viewpost2,viewcomment2
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def FUN_root():
    return render_template("index.html")
    
@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/advertiser")
def advertiser():
    return render_template("advertiser.html")

@app.route("/user")
def user():
       return render_template("user.html")

@app.route("/advertiserreg")
def advertiserreg():
    return render_template("advertiserreg.html")

@app.route("/userreg")
def userreg():
    return render_template("userreg.html")


@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/viewads")
def viewads():
    
    data = view()
    return render_template("viewads.html",add=data)

@app.route("/Chats")
def Chats():
    username = session['username']
    data = view_frd(username)
    return render_template("Chats.html",friend = data)

@app.route("/viewpost")
def viewpost():
    username = session['username']
    data = viewpost1(username)
    data1 = viewcomment1(username)
    return render_template("viewpost.html",post = data, p1=data1)

@app.route("/uvc")
def uvc():
    username = session['username']
    data = viewcomment2(username)
    return render_template("uvc.html",comm = data)

@app.route("/viewcomment")
def viewcomment():
    username = session['username']
    data = viewcomment1(username)
    return render_template("viewcomment.html",comm = data)

@app.route("/analysis")
def analysis():
    username = session['username']
    data = analysis1()
    data3 = analysis2()
    data1 = viewpost1(username)
    return render_template("analysis.html",ana = data, p1=data1,ana1=data3)

@app.route("/vp")
def vp():
    username = session['username']
    data1 = viewpost1(username)
    return render_template("vp.html", p1=data1)



@app.route("/userhome")
def userhome():
    return render_template("userhome.html")

@app.route("/viewrqsts")
def viewrqsts():
    username = session['username']
    data = view_req1(username)
    return render_template("viewrqsts.html",requests = data)

@app.route("/insreq")
def insreq():
    return render_template("insreq.html")

@app.route("/viewusers")
def viewusers():
    data = ins_profile()
    return render_template("viewusers.html",ins = data)

@app.route("/viewadvertisers")
def viewadvertisers():
    data = std_profile()
    return render_template("viewadvertisers.html",stds = data)

@app.route("/adminhome")
def adminhome():
    return render_template("adminhome.html")

@app.route("/adminadvertisements")
def adminadvertisements():
    
    data = view()
    return render_template("adminadvertisements.html",add = data)

@app.route("/viewprofile")
def viewprofile():
    return render_template("viewprofile.html")

@app.route("/advertise")
def advertise():
    return render_template("advertise.html")

@app.route("/vadds")
def vadds():
    username = session['username']
    data = view_req(username)
    return render_template("vadds.html",add = data)

@app.route("/addshome")
def addshome():
    return render_template("addshome.html")


@app.route("/aact",methods = ['GET','POST'])
def aact():
    if request.method == 'POST':
        post=request.form['post']
        print(post)
        data = vaact(post)
        print("....................................")
        print(data)
        return render_template("analysis.html",add1 = data)



@app.route("/pact",methods = ['GET','POST'])
def pact():
    if request.method == 'POST':
        post=request.form['post']
        print(post)
        data = viewpost2(post)
        print("....................................")
        print(data)
        return render_template("viewpost.html",add1 = data)

# -------------------------------Registration-----------------------------------------------------------------    
@app.route("/insreg", methods = ['GET','POST'])
def insreg():
   if request.method == 'POST':    
      
      status = user_reg(request.form['uname'],request.form['mail'],request.form['password'],request.form['gender'],request.form['dob'],request.form['mobile'],request.form['address'])
      
      if status == 1:
       return render_template("user.html",m1="sucess")
      else:
       return render_template("userreg.html",m1="failed")


@app.route("/postact", methods = ['GET','POST'])
def postact():
   if request.method == 'POST':    
      
      status = post_add(request.form['uname'],request.form['post'])
      
      if status == 1:
       return render_template("post.html",m1="sucess")
      else:
       return render_template("post.html",m1="failed")


@app.route("/comment", methods = ['GET','POST'])
def comment():
   if request.method == 'POST':    
      
      status = comment_add(request.form['uname'],request.form['post'],request.form['comment'])
      
      if status == 1:
       return render_template("viewpost.html",m1="sucess")
      else:
       return render_template("viewpost.html",m1="failed")

@app.route("/stdreg", methods = ['GET','POST'])
def stdreg():
   if request.method == 'POST':      
      status = adv_reg(request.form['uname'],request.form['password'],request.form['dob'],request.form['mail'],request.form['mobile'],request.form['address'])
      if status == 1:
       return render_template("advertiser.html",m1="sucess")
      else:
       return render_template("advertiserreg.html",m1="failed")

# #--------------------------------Profile Update-----------------------------------------------------------------

@app.route("/sendmsg", methods = ['GET','POST'])
def sendmsg():
   if request.method == 'POST':      
      status = send_msg(request.form['uname'],request.form['fname'],request.form['msg'])
      if status == 1:
       return render_template("userhome.html",m1="sucess")
      else:
       return render_template("Chats.html",m1="failed")

@app.route("/addadv", methods = ['GET','POST'])
def addadv():
   if request.method == 'POST':  
      username = session['username']    
      status = add_adv(username,request.form['adv'])
      if status == 1:
       return render_template("addshome.html",m1="sucess")
      else:
       return render_template("courses.html",m1="failed")

# # -------------------------------Registration End-----------------------------------------------------------------
# # -------------------------------ADD------------------------------------------------------------------------------
@app.route("/chat", methods = ['GET','POST'])
def chat():
    if request.method == 'POST':
       username = session['username']
       data,data1 = view_msg(username,request.form['fname'])
       
       return render_template("viewmsg.html",msg = data,msg1 = data1)

@app.route("/request")
def request1():
    uname = session['username']
    
    
    status = requestact(uname,request.args.get('fname'))
    return render_template("userhome.html")
    
# #-------------------------------ADD_END---------------------------------------------------------------------------
# # -------------------------------Loginact-----------------------------------------------------------------
@app.route("/adminlogact", methods=['GET', 'POST'])       
def adminlogact():
    if request.method == 'POST':
        status = admin_loginact(request.form['username'], request.form['password'])
        print(status)
        if status == 1:
            session['username'] = request.form['username']
            return render_template("adminhome.html", m1="sucess")
        else:
            return render_template("admin.html", m1="Login Failed")

@app.route("/studentlogact", methods=['GET', 'POST'])       
def studentlogact():
        if request.method == 'POST':
           status = student_loginact(request.form['username'], request.form['password'])
           print(status)
        if status == 1:
            session['username'] = request.form['username']
            return render_template("addshome.html", m1="sucess")
        else:
            return render_template("advertiser.html", m1="Login Failed")

@app.route("/inslogin", methods=['GET', 'POST'])       
def inslogin():
    if request.method == 'POST':
        status = ins_loginact(request.form['username'], request.form['password'])
        print(status)
        if status == 1:
            session['username'] = request.form['username']
            return render_template("userhome.html", m1="sucess")
        else:
            return render_template("user.html", m1="Login Failed")
# # -------------------------------Loginact End-----------------------------------------------------------------

@app.route("/search", methods = ['GET','POST'])
def search():
   if request.method == 'POST':      
      data = c_search(request.form['friend'])
      return render_template("userhome.html",frd = data)
      


    
@app.route("/accept")
def accept():
    uname = session['username']
    status = accept_act(uname,request.args.get('fname'))
    
    if status == 1:
       return render_template("userhome.html",m1="sucess")
    else:
       return render_template("viewrqsts.html",m1="failed")

@app.route("/reject")
def reject():
    uname = session['username']
    status = reject_act(uname,request.args.get('fname'))
    
    if status == 1:
       return render_template("userhome.html",m1="sucess")
    else:
       return render_template("viewrqsts.html",m1="failed")

@app.route("/delete")
def delete():
    
    status = delete_act(request.args.get('id'),request.args.get('uname'),request.args.get('img'))
    
    if status == 1:
       return render_template("addshome.html",m1="sucess")
    else:
       return render_template("/vadds.html",m1="failed")

@app.route("/approve1")
def approve1():
    
    status = approve1_act(request.args.get('username'),request.args.get('mail'))
    
    if status == 1:
       return render_template("viewusers.html",m1="sucess")
    else:
       return render_template("adminhome.html",m1="failed")

@app.route("/reject1")
def reject1():
    
    status = reject1_act(request.args.get('insname'),request.args.get('mail'))
    
    if status == 1:
       return render_template("viewusers.html",m1="sucess")
    else:
       return render_template("adminhome.html",m1="failed")

@app.route("/delete1")
def delete1():
    
    status = delete1_act(request.args.get('id'),request.args.get('uname'),request.args.get('img'))
    
    if status == 1:
       return render_template("adminadvertisements.html",m1="sucess")
    else:
       return render_template("adminhome.html",m1="failed")


   
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
