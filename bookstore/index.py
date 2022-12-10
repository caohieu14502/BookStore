#CONTROLLER
from flask import render_template, request, redirect, url_for
from bookstore import app, login
import utils
import math
from flask_login import login_user, logout_user
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
    # trường name trong input sẽ nhảy vào đây
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
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mật khẩu KHÔNG khớp'
        except Exception as ex:
            err_msg = "Hệ thống có lỗi: " + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['GET', 'POST'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = 'Thông tin đăng nhập KHÔNG chính xác!!!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = utils.get_book_by_id(book_id)
    return render_template('details.html', b=book)


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from bookstore.admin import *
    app.run(debug=True)