from app.models import User
from app import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user,logout_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask import redirect


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class UserView(ModelView):
    column_searchable_list = ['name', 'username']
    column_filters = ['name', 'username']
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
        'name': 'Tên sản phẩm',
        'username':'ten tài khoản'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }

    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin = Admin(app=app, name='Quản trị phòng khám', template_mode='bootstrap4')
admin.add_view(UserView(User,db.session,name='Xem user'))
admin.add_view(StatsView(name='Thông kê'))
admin.add_view(LogoutView(name='Đăng xuất'))