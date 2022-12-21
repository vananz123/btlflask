from app.models import UserRole, NhanVien, BenhNhan, Thuoc, \
    User, LoaiNhanVien, LoaiThuoc, PhieuKham, DonVi_Thuoc, DonVi, QuyDinh,PhieuKham_Thuoc
from app import db, app
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user,logout_user
from flask import redirect
from app.view import yta,admin,bacsi
class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

Admin = Admin(app=app, name='Quản trị phòng khám', template_mode='bootstrap4', index_view=MyAdminView())

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

# admin

Admin.add_view(admin.QLNhanVien(NhanVien, db.session, name='nhân viên',category='Quản lý nhân viên' ))
Admin.add_view(admin.TaoTk( name='Tạo tài khoản',category='Quản lý nhân viên' ))
Admin.add_view(admin.ViewThuoc(Thuoc,db.session, name='Thuốc',category='Quản lý thuốc'))
Admin.add_view(admin.ViewLoaiThuoc(LoaiThuoc, db.session, name='Loại thuốc',category='Quản lý thuốc'))
Admin.add_view(admin.ViewDonVi(DonVi, db.session, name='Đơn vị thuôc',category='Quản lý thuốc'))
Admin.add_view(admin.ViewDonVi_Thuoc(DonVi_Thuoc, db.session, name='giá tiền thuốc trên đơn vị',category='Quản lý thuốc'))
Admin.add_view(admin.ViewQuyDinh(QuyDinh,db.session,name='thay đổi quy định'))
Admin.add_view(admin.ThongKe(name='Thống kê'))
# Y tá
Admin.add_view(yta.DkTrucTiep(BenhNhan, db.session, name='Đăng ký trực tiếp',category='đăng ký trực tiếp'))
#bác sĩ

Admin.add_view(bacsi.TraCuuBN(name='Tra cứu bệnh nhân'))
Admin.add_view(bacsi.PhieuKham(PhieuKham,db.session,name='Phiếu khám'))
Admin.add_view(bacsi.ThemThuoc(PhieuKham_Thuoc,db.session,name='Phiếu khám'))

Admin.add_view(LogoutView(name='Đăng xuất'))