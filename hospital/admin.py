from hospital import app, db, utils
from flask_admin import Admin, BaseView, expose
from hospital.models import Thuoc, QuyDinh, DonViThuoc, LoaiThuoc, UserRole
from flask_admin.contrib.sqla import ModelView
from flask import request, redirect
from flask_login import current_user, logout_user


class StaffView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.STAFF)


class StatsView(BaseView):
    @expose('/')
    def index(self):
        total = 0
        month = request.args.get('month')
        return self.render('admin/stats.html', month_stats=utils.stats_revenue(month), total=utils.total_bill(month))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.STAFF)


class ThuocView(BaseView):
    @expose('/')
    def index(self):
        month=request.args.get('month')
        return self.render('admin/thuoc.html', stats=utils.count_thuoc_by_cate(month))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.STAFF)


class UnitView(StaffView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name']
    column_labels = {
        'id': 'Mã đơn vị',
        'name': 'Tên đơn vị'
    }
    form_excluded_columns = ['medicines']


class CateView(StaffView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name']
    column_labels = {
        'id': 'Mã loại thuốc',
        'name': 'Tên loại thuốc'
    }
    form_excluded_columns = ['medicine']


class MedicineView(StaffView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name']
    column_exclude_list = ['PhieuKham']
    column_labels = {
        'id': 'Mã thuốc',
        'name': 'Tên thuốc',
        'unit_id': 'Đơn vị tính',
        'price': 'Giá tiền',
        'category_id': 'Loại thuốc',
    }
    form_columns = ['name','unit_id','price','category_id']
    form_excluded_columns = ['PhieuKham']


class RuleView(StaffView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name']
    column_labels = {
        'id': 'Mã quy định',
        'name': 'Tên quy định',
        'content': 'Nội dung'
    }
    form_excluded_columns = ['QuyDinh']


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app=app, name='Quản trị', template_mode='bootstrap4')
admin.add_view(MedicineView(Thuoc, db.session, name='Thuốc', category='Quản lý thuốc'))
admin.add_view(CateView(LoaiThuoc, db.session, name='Loại thuốc', category='Quản lý thuốc'))
admin.add_view(UnitView(DonViThuoc, db.session, name='Đơn vị thuốc', category='Quản lý thuốc'))
admin.add_view(RuleView(QuyDinh, db.session, name='Quản lý quy định'))
admin.add_view(StatsView(name='Thống kê doanh thu'))
admin.add_view(ThuocView(name='Thống kê thuốc'))
admin.add_view(LogoutView(name='Đăng xuất'))