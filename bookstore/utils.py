# tương tác csdl - MODEL
from models import Genre, Book, User, Comment, PhieuNhapSach, ChiTietNhapSach, UserRole
from flask_login import current_user
import json
from bookstore import app, db
import hashlib



def load_genres():
    return Genre.query.all()


def load_books(genre_id=None, kw=None, from_price=None, to_price=None, page=1):

    books = Book.query.filter(Book.active.__eq__(True))

    if genre_id:
        books = books.filter(Book.theloai_id == genre_id)
    if kw:
        books = books.filter(Book.name.contains(kw))
    if from_price:
        books = books.filter(Book.price.__ge__(from_price))
    if to_price:
        books = books.filter(Book.price.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return books .slice(start, end).all()


def count_books():
    return Book.query.filter(Book.active.__eq__(True)).count()


def get_book_by_id(book_id):
    return Book.query.get(book_id)


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_comment(book_id, content):
    c = Comment(content=content, book_id=book_id, user=current_user)

    db.session.add(c)
    db.session.commit()

    return c


def get_comments(page=1, book_id=None):

    page_size = app.config['COMMENT_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    c = Comment.query.filter(Comment.book_id == book_id)

    return c.order_by(-Comment.id).slice(start, end).all()

def read_quy_dinh():
    with open('data/quy_dinh_mua_ban.json', "r", encoding='utf8') as f:
        return json.load(f)

def get_hang_ton_co_the_nhap():
    data = read_quy_dinh()

    min_num = 300
    for j in data:
        if j['id'] == 2:
            min_num = j['value']

    return Book.query.filter(Book.stock.__le__(min_num)).all()

def cap_nhat_hang_ton(id, number):

    book_to_update = Book.query.get_or_404(id)
    book_to_update.stock += int(number)

    try:
       db.session.commit()
       return True
    except:
       return False



