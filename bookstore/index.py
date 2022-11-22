#CONTROLLER
from flask import render_template, request
from bookstore import app
import utils

@app.route("/")
def home():
    books = utils.load_books()
    gens = utils.load_genres()
    return render_template('index.html',
                           genres=gens,
                           books=books)

@app.route('/books/<int:book_id>')
def book_detail(book_id) :
    book = utils.get_book_by_id(book_id)
    return render_template('details.html', b=book)

if __name__ == '__main__':
    app.run(debug=True)