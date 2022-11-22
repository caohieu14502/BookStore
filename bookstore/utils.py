# tương tác csdl - MODEL
from models import Genre, Book


def load_genres():
    return Genre.query.all()

def load_books(gen_id=None):

    books =  Book.query.all()
    if (gen_id):
        books = [b for b in books if b['genres_id'] == gen_id]

    return books

def get_book_by_id(book_id):
    return Book.query.get(book_id)