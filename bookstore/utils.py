# tương tác csdl - MODEL
from models import Genre, Book
from bookstore import app

def load_genres():
    return Genre.query.all()

def load_books(genre_id=None, kw=None, page=1):

    books = Book.query.filter(Book.active.__eq__(True))

    if genre_id:
        books = books.filter(Book.theloai_id == genre_id)
    if kw:
        books = books.filter(Book.name.contains(kw))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return books.slice(start, end).all()

def count_books():
    return Book.query.filter(Book.active.__eq__(True)).count()

def get_book_by_id(book_id):
    return Book.query.get(book_id)