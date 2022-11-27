#CONTROLLER
from flask import render_template, request
from bookstore import app
import utils
import math

@app.route("/")
def home():
    nav_index = 0
    books = utils.load_books()
    gens = utils.load_genres()

    genre_id = request.args.get('genre_id')
    kw = request.args.get('keyword')
    if genre_id:
        nav_index = int(genre_id)
    page = request.args.get('page', 1)

    counter = utils.count_books()
    books = utils.load_books(genre_id=genre_id, kw=kw, page=int(page))

    return render_template('index.html',
                           genres=gens,
                           books=books,
                           index=nav_index,
                           page=math.ceil(counter/app.config['PAGE_SIZE']),)

@app.route('/books/<int:book_id>')
def book_detail(book_id) :
    book = utils.get_book_by_id(book_id)
    return render_template('details.html', b=book)

if __name__ == '__main__':
    app.run(debug=True)