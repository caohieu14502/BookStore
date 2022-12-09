# tương tác csdl - MODEL
from models import Genre, Book, User
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

    return books.slice(start, end).all()

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
