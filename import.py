from library import *

import os
import csv
import random



def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        cateid = random.randrange(1,11,1)
        price = random.randrange(5,15,1)
        strprice = str(price)
        db.execute("INSERT INTO book (isbn, title, author ,year, cateid, price, tag) VALUES(:isbn, :title, :author, :year, :cateid, :price, :tag)", {'isbn': isbn, 'title': title, 'author': author, 'year': year, 'cateid':cateid, 'price': price, 'tag': isbn + ',' + author + ',' + author + ',' + year + ',' + strprice})
        print(f'Success {isbn} - {title} - {author} - {year}- {cateid} - {price}$')
    db.commit()
    
if __name__ == "__main__":
    main()
