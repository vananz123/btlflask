from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db,app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum
import hashlib

class UserRole(UserEnum):
    STAFF = 1
    DOCTOR = 2
    NURSE = 3
    ADMIN =4
    USER =5
class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
class User(BaseModel,UserMixin):
    __abstract__ = True
    name = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    username = Column(String(50))
    password = Column(String(50),default='')
    avatar = Column(String(100), default='https://res.cloudinary.com/dg3ozy1rg/image/upload/v1659863226/b0dt6rz11spkeg8bnlht.jpg')
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole),default=UserRole.USER)

class Patient(User):
    __tablename__ ='patient'
    date_of_birth = Column(String(50))
    address = Column(String(200))
    ngayDangKyKham = Column(DateTime(),nullable =True)
    isDanhSach = Column(Boolean(), default=False)
    def __str__(self):
        return self.name

class Staff(User):
    __tablename__ ='staff'
    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all
        db.create_all()
        user = Staff(name='nhat duy', username='nhatduy1', password='c4ca4238a0b923820dcc509a6f75849b', phone='000',
                     avatar='https://res.cloudinary.com/dg3ozy1rg/image/upload/v1659863226/b0dt6rz11spkeg8bnlht.jpg',
                     user_role=UserRole.ADMIN)
        user1 = Patient(name='van an', username='vanan', password='c4ca4238a0b923820dcc509a6f75849b', phone='000',
                        avatar='https://res.cloudinary.com/dg3ozy1rg/image/upload/v1659863226/b0dt6rz11spkeg8bnlht.jpg',
                        date_of_birth='14/444/2002', address='sdfdsf')
        db.session.add(user)
        db.session.add(user1)
        db.session.commit()
















