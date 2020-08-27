from library import *

class Account:

    count = 1

    def __init__(self,id, username, password, email, fullname):
        self.id = Account.count
        Account.count += 1

        self.username = username
        self.password = password
        self.email = email
        self.fullname = fullname
        

    def regestration(self):
        db.execute("INSERT INTO account(id,username,password,email,fullname) VALUES(:id, :username, :password, :email, :fullname)",{'id':self.id, 'username':self.username, 'password':self.password,'email':self.email, 'fullname':self.fullname})
        db.commit()

class Book:
    def __init__(self,isbn, title, author, year, cateid, price):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        
    def bookInsert(self):
        db.execute("INSERT INTO books(isbn,title,author,year,cateid, price) VALUES(:isbn, :title, :author, :year, :cateid, :price)",{'isbn':self.isbn, 'title':self.title, 'author':self.author,'year':self.year, 'cateid':self.cateid, 'price':self.price})
        db.commit()

class star:
    def __init__(self, userID, isbn, star):
        self.userID = userID
        self.isbn = isbn
        self.star = star
    
    def evaluate(self):
        db.execute("INSERT INTO star(userID,isbn,star) VALUES(:userID, :isbn, :star)",{'userID':self.userID, 'isbn':self.isbn, 'star':self.star})
        db.commit()

class review:
    def __init__(self, userID, isbn, review):
        self.userID = userID
        self.isbn = isbn
        self.review = review

    def evaluate(self):
        db.execute("INSERT INTO star(userID,isbn,review) VALUES(:userID, :isbn, :review)",{'userID':self.userID, 'isbn':self.isbn, 'review':self.review})
        db.commit()
    