from models import Genre, Book, User, UserRole
from bookstore import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose, AdminIndexView
from flask import redirect
import utils
from flask import request
from datetime import datetime


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ProductView(AuthenticatedModelView):
    #tìm kiếm theo tên name, author
    column_searchable_list = ['name', 'author', 'theloai_id']
    #cho phép cột nào đc sắp xếp
    column_sortable_list = ['name', 'author', 'price']
    #bỏ cột
    column_exclude_list = ['active']


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        month = request.args.get('month', datetime.now().month)

        return self.render('admin/stats.html',
                           month_stats = utils.book_month_stats(month=month),
                           stats=utils.book_stats(kw=kw, from_date=from_date, to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):

        return self.render('admin/index.html',
                           stats=utils.genre_stats())


admin = Admin(app=app, name="Quản Trị Nhà Sách", template_mode="bootstrap4",
              index_view=MyAdminIndex())
admin.add_view(AuthenticatedModelView(Genre, db.session, name="Thể loại"))
admin.add_view(ProductView(Book, db.session, name="Sách"))
admin.add_view(StatsView(name='Thống kê doanh thu'))
admin.add_view(LogoutView(name='Đăng xuất'))