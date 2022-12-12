#CONTROLLER
import distutils

from flask import render_template, request, redirect, url_for, session, jsonify
from bookstore import app, login
import utils
import math
from models import UserRole
from datetime import date
from flask_login import login_user, logout_user, login_required, current_user
import cloudinary.uploader


@app.route("/")
def home():
    gens = utils.load_genres()

    genre_id = request.args.get('genre_id')
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    page = request.args.get('page', 1)
    sort_high_to_low = request.args.get('htl')


    counter = utils.count_books()
    books = utils.load_books(genre_id=genre_id,
                             kw=kw,
                             from_price=from_price,
                             to_price=to_price,
                             page=int(page))

    books = sorted(books, key=lambda x: x.price)

    if sort_high_to_low: 
        if bool(int(sort_high_to_low)):
            books = sorted(books, key=lambda x: x.price, reverse=True)

    return render_template('index.html',
                           genres=gens,
                           books=books,
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
            url_next = request.args.get('next')

            return redirect(url_next if url_next else '/')
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
    comments = utils.get_comments(request.args.get('page', 1), book_id)

    return render_template('details.html',
                           comments=comments,
                           b=book)


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/api/comments', methods=['post', 'get'])
@login_required
def add_comment():
    data = request.json
    content = data.get('content')
    book_id = int(data.get('book_id'))

    try:
        c = utils.add_comment(content=content, book_id=book_id)
    except:
        return {'status': 404, 'err_msg': 'Có lỗi xảy ra! Vui lòng thử lại sau.'}

    return {'status': 201,
            'comment': {
                'id': c.id,
                'content': c.content,
                'created_date': str(c.created_date),
                'user': {
                    'username': current_user.username,
                    'avatar': current_user.avatar,
                    'name': current_user.name
                }
            }}


@app.route('/inventory', methods=['post', 'get'])
def inventory():
    msg = ''
    if request.method.__eq__('POST'):
        checkboxes = request.form.getlist('book')
        numbers = request.form.getlist('number')
        if checkboxes:
            x = 0
            for c in checkboxes:
                mess = utils.cap_nhat_hang_ton(c, numbers[++x])

            if mess:
                msg = 'Cập nhật thành công'
            else:
                msg = 'Đã xảy ra lỗi, vui lòng thử lại sau'

        redirect(url_for('inventory'))

    genres = utils.load_genres()
    books = utils.get_hang_ton_co_the_nhap()
    quy_dinh = utils.read_quy_dinh()

    min_num = 300
    for j in quy_dinh:
        if j['id'] == 2:
            min_num = j['value']


    return render_template('inventory/inventory.html',
                           books=books,
                           genres=genres,
                           min_num=min_num,
                           date=date.today(),
                           msg=msg)


@app.route('/inventory-login', methods=['post', 'get'])
def signin_inventory():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username,
                                 password=password,
                                 role=UserRole.INVENT_MANAGE)
        if user:
            login_user(user=user)

        return redirect('/inventory')

    return render_template('inventory/login_inventory.html')




if __name__ == '__main__':
    from bookstore.admin import *
    app.run(debug=True)