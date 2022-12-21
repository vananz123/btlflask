from app.models import UserRole
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_login import current_user,logout_user
from wtforms import TextAreaField, validators, Form,StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
from flask import redirect
from app.view import base
from app.dao import *

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class BacSiModelView(base.ManagerView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.DOCTOR
    def is_visible(self):
        return current_user.user_role == UserRole.DOCTOR

class BacSiBaseView(base.BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.DOCTOR
    def is_visible(self):
        return current_user.user_role == UserRole.DOCTOR


class TraCuuBN(BacSiBaseView):
    @expose('/')
    def index(self):
        bn = get_all_bn()
        return self.render('admin/bacsi/tracuu-bn.html',benhnhan =bn)

# class MyForm(Form):
#     ten = StringField('Ten')
class PhieuKham(BacSiModelView):
    column_searchable_list = ['ngayKham']
    column_filters = ['ngayKham']
    can_view_details = True
    can_create = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = dict(trieuChung='Triệu chứng',
                         duDoan='Dự đoán bệnh')
    form_overrides = {
        'description': CKTextAreaField
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

class ThemThuoc(BacSiModelView):
    can_view_details = True
    can_create = True
    can_export = True
    column_exclude_list = ['image']
    form_overrides = {
        'description': CKTextAreaField
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
