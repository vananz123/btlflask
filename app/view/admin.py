from app.models import UserRole,NhanVien,BenhNhan,Thuoc,User,LoaiNhanVien,LoaiThuoc
from app import db, app
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField, validators, Form,StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
from flask import redirect
from app.view import base

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class AdminModelView(base.ManagerView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.ADMIN
    def is_visible(self):
        return current_user.user_role == UserRole.ADMIN

class AdminBaseView(base.BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.ADMIN
    def is_visible(self):
        return current_user.user_role == UserRole.ADMIN
#ModelView
class QuanLyUser(AdminModelView):
    column_searchable_list = ['username']
    column_filters = ['username']
    can_view_details = True
    can_create = False
    can_export = True
    column_exclude_list = ['image']
    column_labels = dict(username='Tên đăng nhập',
                         password='Mật khẩu',
                         user_role='Vai trò',
                         avatar='Ảnh đại diện'
                         )
    form_args = dict(
        username=dict(validators=[DataRequired(), validators.Length(min=5, max=20)],
                      render_kw={
                          'placeholder': 'Tên đăng nhập'
                      })
    )
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
class QLNhanVien(AdminModelView):
    column_searchable_list = ['ten', 'phone']
    column_filters = ['ten', 'phone']
    can_view_details = True
    can_create = False
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }


class ViewThuoc(AdminModelView):
    column_searchable_list = ['ten', 'tacDung']
    column_filters = ['ten', 'tacDung']
    can_view_details = True
    can_create = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = dict( ten='tên thuốc',tacDung='tác dụng')
    form_excluded_columns = ['id','phieukham','donvi']
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }


class ViewLoaiThuoc(AdminModelView):
    column_searchable_list = ['ten']
    column_filters = ['ten']
    can_view_details = True
    can_create = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = dict(ten='tên loại thuốc'
                         )
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
    form_columns = ['ten']

class ViewDonVi(AdminModelView):
    column_searchable_list = ['ten']
    column_filters = ['ten']
    can_view_details = True
    can_create = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = dict(ten='tên đơn vị')
    form_excluded_columns=['thuoc']
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
class ViewDonVi_Thuoc(AdminModelView):
    column_searchable_list = ['giaBan','cachDung']
    column_filters = ['giaBan','cachDung']
    can_view_details = True
    can_create = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = dict(giaBan='giá',donvi='Đơn vị')
    form_excluded_columns=['']
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
class ViewQuyDinh(AdminModelView):
    can_view_details = True
    can_create = False
    can_delete = False
    column_labels = dict(tienKham='tiền khám', soLuong='số lượng khám trong ngày')
    form_excluded_columns = ['']
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
#BaseView
class ThongKe(AdminBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/thongke.html')
    def is_visible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class TaoTk(AdminBaseView):
    @expose('/')
    def index(self):
        loai =LoaiNhanVien.query.all()
        return self.render('admin/create_user.html',loai =loai)