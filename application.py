
from functions import *

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
import pprint

app = Flask(__name__)

# # # Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/home")
def index():
    if session.get('username') == None:
        return render_template('error.html')
    else:
        data = db.execute(
            "SELECT book.isbn, book.title, book.price FROM book LIMIT 24").fetchall()

        list = []
        for tmp in data:

            store = {

                'isbn': tmp['isbn'],
                'title': tmp['title'],
                'price': tmp['price'],

            }

            list.append(store)

        author1 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
            'author': 'Philippa Gregory'}).fetchall()
        author2 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
            'author': 'Nicholas Sparks'}).fetchall()
        author3 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
            'author': 'Louise Penny'}).fetchall()
        author4 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
            'author': 'Patricia Cornwell'}).fetchall()

        name_request = session.get('username')
        name = db.execute('SELECT fullname FROM account WHERE username=:username', {
                          'username': name_request}).first()[0]
        return render_template("home.html", list=list, author1=author1, author2=author2, author3=author3, author4=author4, name=name)


@app.route('/detail/<string:isbn>', methods=['GET'])
def detail(isbn):
    if session.get('username') == None:
        return render_template('error.html')
    else:
        name_db = session.get('username')
        name = db.execute('SELECT fullname FROM account WHERE username=:username', {
                          'username': name_db}).first()[0]
        book = db.execute(
            "SELECT * FROM book WHERE isbn = :isbn", {'isbn': isbn}).first()

        cateID = int(book['cateid'])
        category = db.execute(
            "SELECT * FROM category WHERE id = :id", {'id': cateID}).first()

        category_name = category['name'].title()
        star = round(getStar(isbn), 2)
        review = db.execute(
            "SELECT * FROM review JOIN account ON review.userid = account.id AND review.isbn = :isbn", {'isbn': isbn}).fetchall()

        review_count = db.execute(
            "SELECT COUNT(*) FROM review WHERE isbn = :isbn", {'isbn': isbn}).first()
        review_count = review_count[0]
        star_count = math.floor(star)
        book_same_author = db.execute(
            "SELECT * FROM book WHERE author = :author LIMIT 4", {'author': book['author']}).fetchall()
        return render_template("detail.html", book=book, category=category_name, star=star, review_count=review_count, book_same_author=book_same_author, star_count=star_count, review=review, name=name)


@app.route('/category/<int:id>', methods=['GET'])
def category(id):
    if session.get('username') == None:
        return render_template('error.html')
    else:
        name_db = session.get('username')
        name_account = db.execute('SELECT fullname FROM account WHERE username=:username', {
                                  'username': name_db}).first()[0]
        books = db.execute(
            'SELECT * FROM book WHERE cateid=:cateid', {'cateid': id}).fetchall()
        category = db.execute(
            "SELECT * FROM category WHERE id = :id", {'id': id}).first()
        name = category['name'].title()

        author1 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
                             'author': 'Philippa Gregory'}).fetchall()
        author2 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
                             'author': 'Nicholas Sparks'}).fetchall()
        author3 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
                             'author': 'Louise Penny'}).fetchall()
        author4 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
                             'author': 'Patricia Cornwell'}).fetchall()

        return render_template('category.html', books=books, author1=author1, author2=author2, author3=author3, author4=author4, category=name, name=name_account)


@app.route('/search/', methods=['POST'])
def search():
    if session.get('username') == None:
        return render_template('error.html')
    else:
        name_db = session.get('username')
        name_account = db.execute('SELECT fullname FROM account WHERE username=:username', {
                                  'username': name_db}).first()[0]
        data = request.methods.get('data_search')
        books = db.execute(
            "SELECT * FROM book WHERE tag LIKE %{}%".format(data)).fetchall()

        author1 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
                             'author': 'Philippa Gregory'}).fetchall()
        author2 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
                             'author': 'Nicholas Sparks'}).fetchall()
        author3 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
                             'author': 'Louise Penny'}).fetchall()
        author4 = db.execute("SELECT book.isbn FROM book WHERE author = :author LIMIT 3", {
                             'author': 'Patricia Cornwell'}).fetchall()
        return render_template('category.html', books=books, author1=author1, author2=author2, author3=author3, author4=author4, search=data, name=name_account)


@app.route('/comment', methods=['POST'])
def comment():
    if session.get('username') == None:
        return render_template('error.html')
    else:
        comment = request.form.get('comment')
        isbn = request.form.get('isbn')
        name = session.get('name')
        userid = session.get('id')
        count = db.execute('SELECT COUNT(*) FROM review WHERE userid = :userid AND isbn = :isbn',
                           {'userid': userid, 'isbn': isbn}).first()[0]
        if count == 0:
            db.execute('INSERT INTO review(userid, isbn, review) VALUES(:userid, :isbn, :review)', {
                       'userid': userid, 'isbn': isbn, 'review': comment})
            db.commit()
            return jsonify({'status': True, 'name': name, 'id': userid})
        else:
            return jsonify({'status': False, 'message': "you've been comment already"})


@app.route('/rate', methods = ['POST'])
def rate():
    if session.get('username') == None:
        return render_template('error.html')
    else:
        star = request.form.get('star')
        isbn = request.form.get('isbn')
        userid = session.get('id')
        count = db.execute('SELECT COUNT(*) FROM star WHERE userid = :userid AND isbn = :isbn',
                           {'userid': userid, 'isbn': isbn}).first()[0]
        if count == 0:
            db.execute('INSERT INTO star(userid, isbn, star) VALUES(:userid, :isbn, :star)', {
                       'userid': userid, 'isbn': isbn, 'star': star})
            db.commit()
            new_star = round(getStar(isbn),2)
            return jsonify({'status': True, 'star': new_star, 'message': "rate book successfull"})
        else:
            return jsonify({'status': False, 'message': "you've been rate already"})



@app.route('/api/detail/<string:isbn>', methods=['GET'])
def api(isbn):
    book = db.execute('SELECT * FROM book WHERE isbn = :isbn',{'isbn':isbn}).first()
    rate = db.execute('SELECT SUM(star) as sumStar, COUNT(*) as count FROM star WHERE isbn = :isbn GROUP BY isbn',{'isbn': isbn}).first()
    review = db.execute('SELECT COUNT(*) FROM review WHERE isbn = :isbn',{'isbn':isbn}).first()[0]
    
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "6WOOJNLbybvzYNe3bqydmA", "isbns": isbn})
    data = res.json()
    
    cover = f'http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg'
    rate_count = 0
    count_review = 0;
    if rate != None:
        rate_count = rate['count'] 
    if review != None:
        count_review = review 
    rate_star_count = int(data['books'][0]['work_ratings_count']) + int(rate_count)

    average_star = round(getStar(isbn),2)

    review_count = int(data['books'][0]['work_text_reviews_count']) + int(count_review)

    books = [{
        'id': data['books'][0]['id'],
        'isbn': isbn,
        'title': book['title'],
        'author': book['author'],
        'year': book['year'],
        'cover': cover,
        'count_people_rate_star': rate_star_count,
        'count_people_comment': review_count,
        'average_star': average_star
    }]

    return jsonify({'books': books})


@app.route("/registration")
def registration():
    return render_template('registration.html')


@app.route('/checkRegis', methods=['POST'])
def checkRegis():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    name = request.form.get('name')

    check = db.execute(
        "SELECT COUNT(*) FROM account WHERE username = :username", {'username': username}).first()
    count = check[0]
    if count > 0:
        return jsonify({'status': False, 'message': 'Username already exist'})

    insert = db.execute("INSERT INTO account(username, password, email, fullname) VALUES(:username, :password, :email, :fullname)", {
                        'username': username, 'password': password, 'email': email, 'fullname': name})
    db.commit()
    return jsonify({'status': True, 'message': 'Registration successfull'})


@app.route("/login")
def login():
    return render_template('login.html')


@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    username = request.form.get('username')
    password = request.form.get('password')

    count = db.execute("SELECT COUNT(*) FROM account WHERE username = :username",
                       {'username': username}).first()[0]
    if count != 1:
        return jsonify({'status': False, 'message': "Username don't exist"})
    else:
        query = db.execute(
            "SELECT * FROM account WHERE username = :username", {'username': username}).first()
        password_db = query['password']
        if password == password_db:
            name = db.execute("SELECT id, fullname FROM account WHERE username = :username", {
                              'username': username}).first()
            session['username'] = username
            session['name'] = name['fullname']
            session['id'] = name['id']
            return jsonify({'status': True, 'message': "Login successfull"})

        else:
            return jsonify({'status': False, 'message': "Password is wrong"})


@app.route('/forgot')
def forgotPassword():
    return render_template('forgot_password.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')
