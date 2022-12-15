from app import app,db
from app.models import User
import hashlib
def check_user_register(username):
    try:
        userN = User.query.filter(User.username.__eq__(username.strip())).first()
        if userN:
            return 0
    except(Exception):
        print("loi")
    return 1
