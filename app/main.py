from app import app,db,admin,login
from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from flask_login import login_user, logout_user, current_user
from app.decorators import annonymous_user
from app.models import UserRole

import dao

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/book-in',methods =['get'])
def book_in():
    if current_user.is_authenticated:
        return render_template("book_in.html")
    return render_template('out/login.html')

@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user=user)
        return redirect('/')
    return render_template('out/login.html')

@app.route('/register', methods=['get','post'])
def register():
    msg_err=''
    if request.method.__eq__('POST'):
        password =request.form['password']
        confirm =request.form['confirm']
        if password.__eq__(confirm):
            avatar =''
        try:
            fullname =request.form['firstname'] + request.form['lastname']
            dao.register(name=fullname,username=request.form['username'],password=password,avatar=avatar)
            return redirect('/login')
        except:
            msg_err ='Lỗi'
    return render_template("out/register.html",err_msg=msg_err)

@app.route('/login-admin', methods=['GET', 'POST'])
def admin_login():
    if request.method =="POST":
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username,
                             password=password,role=UserRole.ADMIN)
        if user:
            login_user(user=user)
    return redirect("/admin")
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)
if __name__ == "__main__":
    app.secret_key = 'super secret key'

    app.run(debug=True, port=5000)