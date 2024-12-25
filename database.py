import sqlite3
import hashlib
import datetime
import MySQLdb
from flask import session
from clas_new import* 

def db_connect():
    _conn = MySQLdb.connect(host="localhost", user="root",
                            passwd="root", db="depression")
    c = _conn.cursor()

    return c, _conn



# -------------------------------Registration-----------------------------------------------------------------

def user_reg(uname,mail,password,gender,dob,mobile,address):
    try:
        c, conn = db_connect()
        print(uname,mail,password,gender,dob,mobile,address)
        id="0"
        
        j = c.execute("insert into user (id,name, password, mail,gender,dob,mobile,address) values ('"+id +
                      "','"+uname+"','"+password+"','"+mail+"','"+gender+"','"+dob+"','"+mobile+"','"+address+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def post_add(uname,post):
    try:
        c, conn = db_connect()
        print(uname,post)
        id="0"
        comment1='pending'
        type1=prediction_result(post)
        print("*********************************************")
        print(type1)
        j = c.execute("insert into post (name, post, comment,type) values ('"+uname+"','"+post+"','"+comment1+"','"+type1+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def comment_add(uname,post,comment):
    try:
        c, conn = db_connect()
        print(uname,post)
        id="0"
        #type1='positive'
        print(comment)
        type1=prediction_result(comment)
        print(type1)
        j = c.execute("insert into comment (name, post, comment,type) values ('"+uname+"','"+post+"','"+comment+"','"+type1+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))


def adv_reg(uname, password, dob,mail,mobile,address):
    try:
        c, conn = db_connect()
        print(uname, password, dob,mail,mobile,address)
        id = "0"
        j = c.execute("insert into advetiser (id,username, password, dob,mail,mobile,address) values ('"+id+"','"+uname +
                      "','"+password+"','"+dob+"','"+mail+"','"+mobile+"','"+address+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def update_reg(uname,password,mail,type,image,manager,mobile,address,total):
    try:
        c, conn = db_connect()
        print(uname,password,mail,type,image,manager,mobile,address,total)
        j = c.execute("update user set password='"+password+"',type='"+type+"',image='"+image+"',manager='"+manager+"',mobile='"+mobile+"',address='"+address+"',totstudents='"+total+"' where name='"+uname+"' and mail='"+mail+"'")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))  

def add_course(insname,cname,cost,type,description):
    try:
        c, conn = db_connect()
        print(insname,cname,cost,type,description)
        id = "0"
        j = c.execute("insert into course (id,insname,cname,cost,type,description) values ('"+id +
                      "','"+insname+"','"+cname+"','"+cost+"','"+type+"','"+description+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def requestact(uname,fname):
    try:
        c, conn = db_connect()
        print("xxxxxxxxxxx")
        print(uname,fname)
        id = "0"
        
        j = c.execute("insert into frequest (id,uname,fname,status) values ('"+id +
                      "','"+uname+"','"+fname+"','Pending')")
        conn.commit()
        conn.close()
        print("yyyyyyyyyyyyy")
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def send_msg(uname,fname,msg):
    try:
        c, conn = db_connect()
        print("xxxxxxxxxxx")
        print(uname,fname)
        id = "0"
        
        j = c.execute("insert into chat (id,uname,fname,msg) values ('"+id +
                      "','"+uname+"','"+fname+"','"+msg+"')")
        conn.commit()
        conn.close()
        print("yyyyyyyyyyyyy")
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def add_adv(username,adv):
    try:
        c, conn = db_connect()
        print("xxxxxxxxxxx")
        print(username,adv)
        id = "0"
        
        j = c.execute("insert into adds (id,username,img) values ('"+id +"','"+username+"','"+adv+"')")
        conn.commit()
        conn.close()
        print("yyyyyyyyyyyyy")
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def view_msg(username,fname):
    c, conn = db_connect()
    c.execute("select * from chat where fname='"+fname+"'")
    result = c.fetchall()
    
    c.execute("select * from frequest where uname='"+username+"' and fname='"+fname+"'")
    result1 = c.fetchall()
    conn.close()
    print("result")
    return result,result1

def ins_profile():
    c, conn = db_connect()
    c.execute("select * from user")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def view_std(name):
    c, conn = db_connect()
    c.execute("select * from regcourses where insname = '"+name+"'")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def c_search(friend):
    c, conn = db_connect()
    c.execute("select * from user where name  like'"+friend+"' ")
    result = c.fetchall()
    conn.close()
    print(result)
    return result
              
def accept_act(uname,fname):
    c, conn = db_connect()
    status = "Accepted"
    j = c.execute("update frequest set status='"+status+"' where fname='"+uname+"'  ")
    conn.commit()
    conn.close()
    return j

def reject_act(uname,fname):
    c, conn = db_connect()
    status = "Rejected"
    j = c.execute("update frequest set status='"+status+"' where uname='"+uname+"' and fname='"+fname+"'")
    conn.commit()
    conn.close()
    return j


def approve1_act(username,mail):
    c, conn = db_connect()
    status = "Approved"
    j = c.execute("update user set status='"+status+"' where  name='"+username+"' and mail='"+mail+"'")
    conn.commit()
    conn.close()
    return j

def reject1_act(username,mail):
    c, conn = db_connect()
    status = "Rejected"
    j = c.execute("update user set status='"+status+"' where  name='"+username+"' and mail='"+mail+"'")
    conn.commit()
    conn.close()
    return j


def std_profile():
    c, conn = db_connect()
    c.execute("select * from advetiser")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def view_req(username):
    c, conn = db_connect()
    c.execute("select * from adds where username='"+username+"'")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def view_req1(username):
    c, conn = db_connect()
    c.execute("select * from frequest where fname='"+username+"'  ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def viewpost1(username):
    c, conn = db_connect()
    c.execute("select * from post")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


def viewpost2(post):
    c, conn = db_connect()
    c.execute("select * from post where post='"+post+"'")
    result = c.fetchall()
    conn.close()
    print("result")
    return result



def viewcomment1(username):
    c, conn = db_connect()
    c.execute("select * from post where name='"+username+"' ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


def viewcomment2(username):
    c, conn = db_connect()
    c.execute("select * from post where name='"+username+"' ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def analysis1():
    c, conn = db_connect()
    c.execute("select count(type) from post where type='Depressiontweet'")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


def analysis2():
    c, conn = db_connect()
    c.execute("select count(type) from post where type='Normaltweet'")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


def vaact(post):
    print("22222222222")
    print(post)
    c, conn = db_connect()
    c.execute("select count(type) from comment where  type='positive' and post='"+post+"'")
    result = c.fetchall()
    print(".....................................123")
    print(result)
    conn.close()
    print("result")
    return result


def view_frd(username):
    c, conn = db_connect()
    c.execute("select * from frequest where uname='"+username+"' and status = 'Accepted' ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


              
def delete_act(id,uname,img):
    c, conn = db_connect()
    j = c.execute("delete from adds where id='"+id+"' and username='" +
                  uname+"' and img='"+img+"'")
    conn.commit()
    conn.close()
    return j

def delete1_act(id,uname,img):
    c, conn = db_connect()
    j = c.execute("delete from adds where id='"+id+"' and username='" +
                  uname+"' and img='"+img+"'")
    conn.commit()
    conn.close()
    return j



def view():
    c, conn = db_connect()
    c.execute("select * from adds ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result
              









                        
# # -------------------------------Registration End-----------------------------------------------------------------
# # -------------------------------Loginact Start-----------------------------------------------------------------

def admin_loginact(username, password):
    try:
        c, conn = db_connect()
        j = c.execute("select * from admin where username='" +
                      username+"' and password='"+password+"'")
        c.fetchall()
        conn.close()
        return j
    except Exception as e:
        return(str(e))

def student_loginact(username, password):
    try:
        c, conn = db_connect()
        j = c.execute("select * from advetiser where username='" +
                      username+"' and password='"+password+"'")
        c.fetchall()
        conn.close()
        return j
    except Exception as e:
        return(str(e))

def ins_loginact(username, password):
    try:
        c, conn = db_connect()
        
        j = c.execute("select * from user where name='" +
                      username+"' and password='"+password+"' "  )
        c.fetchall()
        conn.close()
        return j
    except Exception as e:
        return(str(e))

if __name__ == "__main__":
    print(db_connect())
