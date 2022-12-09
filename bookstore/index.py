#CONTROLLER
from flask import render_template, request, redirect, url_for
from bookstore import app
import utils
import math
import cloudinary.uploader

@app.route("/")
def home():
    nav_index = 0
    books = utils.load_books()
    gens = utils.load_genres()

    genre_id = request.args.get('genre_id')
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    if genre_id:
        nav_index = int(genre_id)
    page = request.args.get('page', 1)

    counter = utils.count_books()
    books = utils.load_books(genre_id=genre_id,
                             kw=kw,
                             from_price=from_price,
                             to_price=to_price,
                             page=int(page))

    return render_template('index.html',
                           genres=gens,
                           books=books,
                           index=nav_index,
                           page=math.ceil(counter/app.config['PAGE_SIZE']),)

@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    #trường name trong input sẽ nhảy vào đây
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name,
                               username=username,
                               password=password,
                               email=email,
                               avatar=avatar_path)
                return redirect('index.html')
            else:
                err_msg = 'Mật khẩu KHÔNG khớp'
        except Exception as ex:
            err_msg = "Hệ thống có lỗi: " + str(ex)

    return render_template('register.html', err_msg=err_msg)

@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = utils.get_book_by_id(book_id)
    return render_template('details.html', b=book)

if __name__=='__main__':
    app.run(debug=True)