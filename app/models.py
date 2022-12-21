from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum,DECIMAL
from sqlalchemy.orm import relationship
from app import db,app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum
import hashlib

class UserRole(UserEnum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    STAFF =4
    USER =5
class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
#NGUOI DUNG
class User(BaseModel,UserMixin):
    __tablename__='User'
    username = Column(String(50),default='')
    password = Column(String(50),default='')
    avatar = Column(String(100), default='https://res.cloudinary.com/dg3ozy1rg/image/upload/v1659863226/b0dt6rz11spkeg8bnlht.jpg')
    user_role = Column(Enum(UserRole),default=UserRole.USER)
    nhanvien = relationship('NhanVien', backref='User', lazy=True)
    admin = relationship('Admin', backref='User', lazy=True)
    def __str__(self):
        return self.username
    def set_password(self, password):
        self.password = hashlib.md5(password.encode('utf8')).hexdigest()
class LoaiNhanVien(BaseModel):
    __tablename__='LoaiNhanVien'
    ten = Column(String(50), nullable=False)
    nhanvien = relationship('NhanVien', backref='LoaiNhanVien', lazy=True)
    def __str__(self):
        return self.ten
class LichKham(BaseModel):
    __tablename__ ='LichKham'
    lichKham =Column(String(50), nullable =False)
    isDanhSach =Column(Boolean(), default =False)
    soLuong = Column(Integer, default=0)
    benhnhan = relationship('LichKham_BenhNhan', backref='LichKham', lazy=True)
    def __str__(self):
        return self.lickKham
class BenhNhan(BaseModel):
    __tablename__ ='BenhNhan'
    ten = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False,unique=True)
    namSinh = Column(String(50),nullable=False)
    diaChi = Column(String(200),nullable=False)
    gioiTinh =Column(Boolean(), nullable=False)

    phieukham=relationship('PhieuKham', backref='BenhNhan', lazy=True)
    lichkham = relationship('LichKham_BenhNhan',backref='BenhNhan', lazy=True)

    def __str__(self):
        return self.ten

class LichKham_BenhNhan(BaseModel):
    __tablename__ ='LichKham_BenhNhan'
    benhnhan_id = Column(Integer,ForeignKey(BenhNhan.id),nullable=False)
    lichkham_id =Column(Integer,ForeignKey(LichKham.id),nullable=False)


class NhanVien(db.Model):
    __tablename__ ='NhanVien'
    user_id = Column(Integer, ForeignKey(User.id),primary_key=True)
    loai_id = Column(Integer, ForeignKey(LoaiNhanVien.id),nullable=False)
    ten = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    phieukham =relationship('PhieuKham', backref='NhanVien', lazy=True)
    hoadon = relationship('HoaDon', backref='NhanVien', lazy=True)
    def __str__(self):
        return self.ten

class Admin(db.Model):
    __tablename__='Admin'
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    mail = Column(String(50), nullable=False)
    def __str__(self):
        return self.mail

class QuyDinh(BaseModel):
    __tablename__ ='QuyDinh'
    tienKham =Column(DECIMAL,default =0.0)
    soLuong =Column(Integer,default =40)
#PHIEU
class PhieuKham(BaseModel):
    __tablename__='PhieuKham'
    benhnhan_id =Column(Integer,ForeignKey(BenhNhan.id),nullable= False)
    nhanvien_id= Column(Integer,ForeignKey(NhanVien.user_id) ,nullable =False)
    ngayKham =Column(String(50),default= datetime.now())
    trieuChung =Column(String(300),nullable=False)
    duDoan = Column(String(300), nullable=False)
    hoadon =relationship('HoaDon',backref='PhieuKham', lazy=True )
    thuoc =relationship('PhieuKham_Thuoc', backref='thuoc', lazy=True)
#THUOC
class LoaiThuoc(BaseModel):
    __tablename__='LoaiThuoc'
    ten =Column(String(100),nullable =False)
    thuoc =relationship('Thuoc',backref='LoaiThuoc', lazy=True)
    def __str__(self):
        return self.ten
class DonVi(BaseModel):
    __tablename__='DonVi'
    ten =Column(String(50),nullable =False)
    thuoc =relationship('DonVi_Thuoc',backref='DonVi', lazy=True)
    def __str__(self):
        return self.ten
class Thuoc(BaseModel):
    __tablename__='Thuoc'
    loaithuoc_id =Column(Integer,ForeignKey(LoaiThuoc.id),nullable= False)
    ten =Column(String(100),nullable =False)
    tacDung =Column(String(200),nullable =False)
    donvi =relationship('DonVi_Thuoc',backref='Thuoc', lazy=True)
    phieukham =relationship('PhieuKham_Thuoc', backref='Thuoc', lazy=True)
    def __str__(self):
        return self.ten
class DonVi_Thuoc(BaseModel):
    __tablename__= 'DonVi_Thuoc'
    giaBan =Column(DECIMAL, default =0.0)
    cachDung =Column(String(100),nullable =False)
    thuoc_id = Column(Integer,ForeignKey(Thuoc.id),nullable= False)
    donvi_id =Column(Integer,ForeignKey(DonVi.id),nullable =False)
class HoaDon(BaseModel):
    __tablename__='HoaDon'
    phieukham_id =Column(Integer,ForeignKey(PhieuKham.id),nullable=False)
    nhanvien_id= Column(Integer,ForeignKey(NhanVien.user_id) ,nullable =False)
    tienThuoc =Column(DECIMAL,default =0.0)
    tongTien = Column(DECIMAL,default =0.0)
    ngayThanhToan = Column(DateTime(), default=datetime.now())
    isThanhToan =Column(Boolean(), default = False)

class PhieuKham_Thuoc(BaseModel):
    __tablename__ ='PhieuKham_Thuoc'
    thuoc_id =Column(Integer,ForeignKey(Thuoc.id),nullable=False)
    phieukham_id =Column(Integer,ForeignKey(PhieuKham.id),nullable=False)

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all
        db.create_all()
        s1 = LoaiNhanVien(ten='Doctor')
        s2 = LoaiNhanVien(ten='Staff')
        s3 = LoaiNhanVien(ten='Nuser')
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()
        user = User(username='vanan', password='c4ca4238a0b923820dcc509a6f75849b', user_role=UserRole.ADMIN)
        user1 = User(username='vanan1', password='c4ca4238a0b923820dcc509a6f75849b')
        user2 = User(username='vanan2', password='c4ca4238a0b923820dcc509a6f75849b', user_role=UserRole.DOCTOR)
        db.session.add(user)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        ad = Admin(user_id=user.id, mail='@fghfg')
        sta = NhanVien(user_id=user2.id, loai_id=s1.id, ten='Van hoai ', phone='0000')
        db.session.add_all([ad, sta])
        db.session.commit()


















