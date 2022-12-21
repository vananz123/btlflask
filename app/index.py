from app import app,db,init_admin,login, controllers
import utils
import dao
import cloudinary.uploader

app.add_url_rule('/','index',controllers.home)
app.add_url_rule('/login','login-user',controllers.login_my_user,methods=['get','post'])
app.add_url_rule('/register','register-user',controllers.register,methods=['get','post'])
app.add_url_rule('/logout','logout-user',controllers.logout,methods=['get','post'])
app.add_url_rule('/profile','profile-user',controllers.profile_user)
app.add_url_rule('/admin/create_user','create-user',controllers.create_user,methods=['post'])
app.add_url_rule('/api/tracuu','tra_cuu',controllers.tra_cuu,methods=['post'])
app.add_url_rule('/bacsi/thongtin','thongtin',controllers.thongtin_bs)
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)
if __name__ == "__main__":
    app.secret_key = 'super secret key'

    app.run(debug=True, port=5000)