from models import Genre, Book, User
from bookstore import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app=app, name="Quản Trị Nhà Sách", template_mode="bootstrap4")

admin.add_view(ModelView(Genre, db.session, name="Thể loại"))
admin.add_view(ModelView(Book, db.session, name="Sách"))
