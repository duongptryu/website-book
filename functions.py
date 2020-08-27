import os
from library import *
from flask import jsonify
import math, requests


def getAll():
    data = db.execute("SELECT book.isbn, book.title, book.price FROM book LIMIT 24").fetchall()
    return data

def getBookByCate(category):
    cateID  = db.execute("SELECT id FROM category WHERE name = :name",{'name':category}).first()

    data = db.execute("SELECT isbn, title FROM book WHERE cateid = :cateid",{'cateid':cateID}).fetchall()
    return data

def searchByISBN(isbn):
    data = db.execute("SELECT isbn, title FROM  BOOK WHERE isbn LIKE %:isbn%",{'isbn':isbn}).fetchall()
    return data

def searchByTitle(title):
    data = db.execute("SELECT isbn, title FROM  BOOK WHERE title LIKE %:title%",{'title':title}).fetchall()
    return data


def searchByCategory(category):
    cateID  = db.execute("SELECT id FROM category WHERE name like %:name%",{'name':category}).fetchall()

    data = db.execute("SELECT isbn, title FROM  BOOK WHERE cateid IN :cateid",{'cateid':cateID}).fetchall()
    return data

def searchByAuthor(author):
    data = db.execute("SELECT isbn, title FROM  BOOK WHERE author LIKE %:author%",{'author':author}).fetchall()
    return data

def searchByPrice(price):
    data = db.execute("SELECT isbn, title FROM  BOOK WHERE price LIKE %:price%",{'price':price}).fetchall()
    return data

def getBookDetail(isbn):
    data = []
    info_book = db.execute("SELECT * FROM book WHERE isbn = :isbn",{'isbn':isbn}).first()
    star = db.execute("SELECT star FROM star WHERE isbn = :isbn",{'isbn':isbn}).fetchall()
    if star['star'] == None:
        star['star'] = 0;
    review = db.execute("SELECT review FROM revire WHERE isbn = :isbn",{'isbn':isbn}).fetchall()
    data.append(info_book)
    data.append(star)
    data.append(review)
    return data

def login(username, password):
    data = db.execute("SELECT * FROM account WHERE username = :username",{'username':username}).first()

    if data == None:
        return jsonify({'status': False, 'message':'Invalid username'})
    else:
        if data['password'] != password:
            return jsonify({'status': False, 'message':'Invalid password'})
        else:
            return jsonify({'status': True, 'message':'Login success'})
    
def getStar(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "6WOOJNLbybvzYNe3bqydmA", "isbns": isbn})
    data = res.json()
    count_api = data['books'][0]['work_ratings_count']
    average_api = data['books'][0]['average_rating']
    sumStar_api = float(average_api)*count_api
    sumStar_db = 0
    request_db = db.execute("SELECT SUM(star) as star FROM star WHERE isbn = :isbn GROUP BY isbn", {'isbn':isbn}).first()
    if request_db != None:
        sumStar_db = request_db['star']
    count_db = db.execute("SELECT COUNT(*) FROM star WHERE isbn = :isbn", {'isbn':isbn}).first()
    count = count_db[0]
    if sumStar_db == None:
            sumStar_db = 0
    sumStar = sumStar_api + sumStar_db
    sumCount = float(count) + float(count_api)
    average = sumStar/sumCount
    return average 
