from app.models import Patient,Staff
from app import db
from app.models import UserRole
import hashlib

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return Patient.query.filter(Patient.username.__eq__(username.strip()), Patient.password.__eq__(password)).first()

def auth_admin(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Staff.query.filter(Staff.username.__eq__(username.strip()), Staff.password.__eq__(password)).first()

def register(name, username, password, avatar,phone):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u =Patient(name=name, username=username.strip(), password=password,avatar=avatar,phone=phone)
    db.session.add(u)
    db.session.commit()

def get_user_by_id(user_id):
    return Patient.query.get(user_id)

