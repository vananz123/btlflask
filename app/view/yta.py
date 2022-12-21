from app.models import UserRole,NhanVien,BenhNhan,Thuoc,User,LoaiNhanVien,LoaiThuoc
from flask_login import current_user,logout_user
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

class YTaView(base.ManagerView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.NURSE
    def is_visible(self):
        return current_user.user_role == UserRole.NURSE

class MyForm(Form):
    ten = StringField('Ten')
class DkTrucTiep(YTaView):
    column_searchable_list = ['ten', 'phone']
    column_filters = ['ten', 'phone']
    can_view_details = True
    can_create = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = dict(ten='tên bệnh nhân',
                         phone='số điện thoại',
                         namSinh='Ngày sinh',
                         diaChi='địa chỉ',
                         gioiTinh='giới tính (không tích là Nam, tích là Nữ)')
    form_columns = ['ten','phone','namSinh','diaChi','gioiTinh']
    form_overrides = {
        'description': CKTextAreaField
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
