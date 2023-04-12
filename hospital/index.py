from hospital import utils, app, models, controllers, login
from hospital.admin import *


@login.user_loader
def get_staff(nhan_vien_id):
    return utils.get_staff_by_id(nhan_vien_id)


app.add_url_rule('/', 'home', controllers.home)

app.add_url_rule('/admin', 'admin', controllers.admin, methods=["POST"])

app.add_url_rule('/register', 'register', controllers.index, methods=['get', 'post'])

app.add_url_rule('/create', 'create_list', controllers.create_list)

app.add_url_rule('/add-date', 'add_date', controllers.add_date, methods=['get', 'post'])

app.add_url_rule('/login', 'login', controllers.login)

app.add_url_rule('/staff-user', 'staff_user', controllers.staff_user, methods=['get', 'post'])

app.add_url_rule('/phieu-kham', 'phieukham', controllers.phieukham)

app.add_url_rule('/tracuuthuoc', 'tracuuthuoc', controllers.tracuuthuoc, methods=['get', 'post'])

app.add_url_rule('/lichsu', 'lichsu', controllers.lichsu, methods=['get', 'post'])

app.add_url_rule('/phieu-kham', 'benhnhan', controllers.benhnhan, methods=['get', 'post'])

app.add_url_rule('/api/create', 'create', controllers.create, methods=["POST"])

app.add_url_rule('/api/add-thuoc', 'thuoc', controllers.thuoc, methods=["POST"])

app.add_url_rule('/don-thuoc', 'donthuoc', controllers.donthuoc, methods=['get', 'post'])

app.add_url_rule('/pay', 'pay', controllers.pay, methods=['get', 'post'])

app.add_url_rule('/payall', 'payall', controllers.payall, methods=['get', 'post'])

app.add_url_rule('/tracuuthuoc', 'tracuuthuoc', controllers.tracuuthuoc, methods=['get', 'post'])

app.add_url_rule('/logout', "logout_my_user", controllers.logout_my_user)

if __name__ == '__main__':
    app.run(debug=True)
