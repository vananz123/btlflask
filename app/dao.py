from app.models import BenhNhan,NhanVien,UserRole,User,Admin,\
    LoaiNhanVien,LichKham,LichKham_BenhNhan,QuyDinh,PhieuKham,PhieuKham_Thuoc
from flask import session
from app import db
from sqlalchemy import Column, Integer,update
import hashlib

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u= User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()
    return u

def register(name, username, password, avatar,phone):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user =User(username=username.strip(),password=password,avatar=avatar)
    db.session.add(user)
    db.session.commit()
    bn =BenhNhan(user_id=user.id, name=name,phone=phone)
    db.session.add(bn)
    db.session.commit()
def create_user(name, username, password, avatar,phone,loai):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user =User(username=username.strip(),password=password,avatar=avatar,user_role =user_role(loai))
    db.session.add(user)
    db.session.commit()
    nv =NhanVien(user_id=user.id,loai_id=int(loai), ten=name,phone=phone)
    db.session.add(nv)
    db.session.commit()
def tao_lickkham(lichKham):
    lk1 = LichKham(lichKham=lichKham, soLuong=1)
    db.session.add(lk1)
    db.session.commit()
    return lk1
def tao_bn(ten,phone,namSinh,diaChi,gioiTinh):
    if gioiTinh =='0':
        gioiTinh =0
    else:
        gioiTinh=1

    bn =BenhNhan(ten=ten,phone=phone,namSinh=namSinh,diaChi=diaChi,gioiTinh=gioiTinh)
    db.session.add(bn)
    db.session.commit()
    return bn
def controller_dangky(lichKham,bn_id):
    lk =LichKham.query.filter(LichKham.lichKham ==lichKham).first()
    bn = BenhNhan.query.get(int(bn_id))
    if lk:
        qd = int(QuyDinh.query.get(1).soLuong)
        if lk.soLuong <= qd:
            lk.soLuong =int(lk.soLuong)+1
            db.session.commit()
        else:
            return bn
    else:
        lk =tao_lickkham(lichKham)
    db.session.add(LichKham_BenhNhan(lichkham_id=lk.id, benhnhan_id=bn.id))
    db.session.commit()
    return ''
def check_bn(phone):
    bn = BenhNhan.query.filter(BenhNhan.phone == phone).first()
    if bn:
        return bn
    else:
        return ''
def get_user_by_id(user_id):
    return User.query.get(user_id)
def get_bacsi_all():
    return db.session.query(NhanVien.user_id,NhanVien.ten,NhanVien.phone)\
            .join(LoaiNhanVien,LoaiNhanVien.id.__eq__(NhanVien.loai_id)) \
            .filter(LoaiNhanVien.ten.__eq__("Doctor")).all()
def user_role(loai):
    if loai == '1':
        return UserRole.ADMIN
    elif loai == '2':
        return UserRole.DOCTOR
    elif loai == '3':
        return UserRole.NURSE
    else:
        return UserRole.STAFF

# def tracuu_bn(kw):
#     query = db.session.query(BenhNhan.id,BenhNhan.ten,BenhNhan.namSinh,BenhNhan.diaChi)\
#     .join(PhieuKham, PhieuKham.benhnhan_id.__eq__(BenhNhan.id)) \
#         .join(PhieuKham_Thuoc, PhieuKham_Thuoc.phieukham_id.__eq__(PhieuKham.id))
#     if kw:
#         query = query.filter(BenhNhan.ten.contains(kw))
#
#     return query.all()
def get_all_bn():
    return db.session.query(BenhNhan).all()
