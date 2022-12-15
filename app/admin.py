from app.models import UserRole,Staff,Patient
from app import db, app
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user,logout_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask import redirect

class ManagerView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return current_user.is_authenticated

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class UserView(ManagerView):
    column_searchable_list = ['name', 'phone']
    column_filters = ['name', 'phone']
    can_view_details = True
    can_create = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)
class CreatePa(ModelView):
    column_searchable_list = ['name', 'phone']
    column_filters = ['name', 'phone']
    can_view_details = True
    can_create = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.NURSE)

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html',)
admin = Admin(app=app, name='Quản trị phòng khám', template_mode='bootstrap4',index_view=MyAdminView())
admin.add_view(UserView(Staff,db.session,name='Quản lý nhân viên'))
admin.add_view(CreatePa(Patient,db.session,name='Tạo bệnh nhân'))
admin.add_view(LogoutView(name='Đăng xuất'))