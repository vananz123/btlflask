from datetime import datetime

from app import app,db,init_admin,login
from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from flask_login import login_user, logout_user, current_user
from app.decorators import annonymous_user
from app.models import UserRole,NhanVien,User,BenhNhan
import utils
import dao
import json
import cloudinary.uploader

def home():
    return render_template("home.html")

@app.route('/dangkykham',methods =['post','get'])
def dang_ky_kham():
    if request.method =='POST':
        phone = request.form['phone']
        print(phone)
        check = dao.check_bn(phone)
        print(check.ten)
        if check != '':
            return render_template('clinet/form.html', bn=check)
        else:
            return render_template('clinet/create_bn.html')

    return render_template('clinet/dangkykham.html')
@app.route('/dangkykham/create',methods =['post'])
def dang_ky_kham_create():
    ten = request.form['name']
    phone = request.form['phone']
    namSinh = request.form['namesinh']
    diaChi = request.form['address']
    gioiTinh = request.form['gt']
    bn = dao.tao_bn(ten=ten, phone=phone, namSinh=namSinh, diaChi=diaChi, gioiTinh=gioiTinh)
    return render_template('clinet/form.html',bn=bn)

@app.route('/dangkykham/form',methods =['post'])
def dang_ky_kham_form():
    lichKham =request.form['lichkham']
    bn_id=request.form['bn_id']
    check =dao.controller_dangky(lichKham,bn_id)
    if check =='':
        return render_template('clinet/success.html')
    return redirect('/dangkykham/form',bn=check)



def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user=user)
        return redirect('/admin')
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

# @app.route('/api/register',methods=['post'])
# def check_register():
#     data =request.json
#     username= data['username']
#     password = data['password']
#     confirm = data['confirm']
#     print(password,confirm)
#     key = app.config['USER_KEY']
#     return utils.check_user_register(username=username)
def create_user():
    msg_err = ''
    if request.method.__eq__('POST'):
        phone = request.form['phone']
        password = request.form['password']
        confirm = request.form['confirm']
        username = request.form['username']
        loai=request.form['loai']
        print(type(loai))
        if password.__eq__(confirm):
            avatar = 'https://res.cloudinary.com/dg3ozy1rg/image/upload/v1659863226/b0dt6rz11spkeg8bnlht.jpg'
            try:
                fullname = request.form['firstname'] + request.form['lastname']
                dao.create_user(name=fullname, username=username, password=password, avatar=avatar, phone=phone,loai=loai)
            except:
                msg_err = 'Lỗi'
        else:
            msg_err = "Lôi pass"
    return redirect('/admin/nhanvien')
def get_bn_ten(ten):
    return BenhNhan.query.filter(BenhNhan.ten.__eq__(ten.strip())).all()
def tra_cuu():
    data =request.json
    kw = str(data['ten'])
    print(kw)
    bn = dao.tracuu_bn(kw)
    data =[]
    for i in bn:
        data.append({
            'id':i.id,
            'ten':i.ten,
            'namsinh':i.namSinh,
            'diachi':i.diaChi
        })
    return bn
def thongtin_bs():
    a =dao.get_bacsi_all()
    print(a)
    return render_template('bacsi.html',bacsi=a)
def profile_user():
    return render_template("profile.html")
def logout():
    logout_user()
    return redirect('/')