from app import app,db,admin,login, controllers
from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from flask_login import login_user, logout_user, current_user
from app.decorators import annonymous_user
from app.models import UserRole,Staff
import utils
import dao
import cloudinary.uploader

app.add_url_rule('/','index',controllers.home)
app.add_url_rule('/login','login-user',controllers.login_my_user,methods=['get','post'])
app.add_url_rule('/login-admin','admin-login',controllers.admin_login,methods=['get','post'])
app.add_url_rule('/register','register-user',controllers.register,methods=['get','post'])
app.add_url_rule('/logout','logout-user',controllers.logout,methods=['get','post'])
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)
if __name__ == "__main__":
    app.secret_key = 'super secret key'

    app.run(debug=True, port=5000)