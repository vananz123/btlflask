from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from flask_login import current_user

from flask import redirect

class ManagerView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return current_user.is_authenticated

class BaseView(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return current_user.is_authenticated