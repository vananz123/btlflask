from app import app,db,admin,login
from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from flask_login import login_user, logout_user, current_user
from app.decorators import annonymous_user
from app.models import UserRole,Staff
import utils
import dao
import cloudinary.uploader

def home():
    return render_template("home.html")

@app.route('/book-in',methods =['get'])
def book_in():
    if current_user.is_authenticated:
        return render_template('book_in.html')
    return render_template('out/login.html')

@annonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user=user)
        return redirect('/')
    return render_template('out/login.html')

def register():
    msg_err=''
    if request.method.__eq__('POST'):
        phone =request.form['phone']
        password =request.form['password']
        confirm =request.form['confirm']
        username =request.form['username']
        if password.__eq__(confirm):
            avatar ='https://res.cloudinary.com/dg3ozy1rg/image/upload/v1659863226/b0dt6rz11spkeg8bnlht.jpg'
            try:
                fullname = request.form['firstname'] + request.form['lastname']
                dao.register(name=fullname, username=username, password=password, avatar=avatar,phone=phone)
                return redirect('/login')
            except:
                msg_err ='Lỗi'
        else:
            msg_err="Lôi pass"
    return render_template("out/register.html",err_msg=msg_err)

@app.route('/api/register',methods=['post'])
def check_register():
    data =request.json
    username= data['username']
    password = data['password']
    confirm = data['confirm']
    print(password,confirm)
    key = app.config['USER_KEY']
    return utils.check_user_register(username=username)

def admin_login():
    if request.method =="POST":
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_admin(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect("/admin")
    return redirect('/')

def logout():
    logout_user()
    return redirect('/')