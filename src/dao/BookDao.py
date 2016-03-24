'''
Created on 02-Dec-2015

@author: vijay
'''

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, \
    Column, Integer, String, Column, Integer, String, create_engine, create_engine
from sqlalchemy.ext.declarative import declarative_base, declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import os
import sys
import sqlalchemy
from src.dao.Author import Author
from src.dao.AuthorBookLink import AuthorBookLink, AuthorBookLink
import json
from src.dao.Book import Base, Book
from src.dao.Book import engine
import shutil
import traceback
from src.static.constant import Workspace
import datetime
from src.static.SessionUtil import SingletonSession

#  def getSession(self):
print '3--->', os.getcwd(), os.name, sys.platform

if os.path.exists(Workspace().path):
    os.chdir(Workspace().path)
    listOfDir = os.listdir(Workspace().path)
    
 
class CreateDatabase():

    def __init__(self):
        self.engine = create_engine('sqlite:///' + Workspace().path + os.sep + '_opal.sqlite', echo=True)
        Session = sessionmaker(autoflush=True, autocommit=False, bind=self.engine)
        self.session = SingletonSession().session
        
        if not os.path.exists(Workspace().path):
            os.mkdir(Workspace().path)
        os.chdir(Workspace().path)
        

    def creatingDatabase(self):
        os.chdir(Workspace().path)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)


    def addingData(self):

        directory_name = Workspace().path
        os.chdir(directory_name)
        listOfDir = [ name for name in os.listdir(directory_name) if os.path.isdir(os.path.join(directory_name, name)) ]
        if listOfDir:
            listOfDir.sort(key=int)
        one = ''
       
            
        for sName in listOfDir:
            one = os.path.join(directory_name , sName)
            file = open(os.path.join(one , 'book.json'), 'r')

            rep = ''
            for line in file:
                rep = rep + line
            file.close
            b = json.loads(rep)
            book = Book()
            for k in b:
                if not isinstance(b[k], list):
                    if k in ['publishedOn', 'createdOn']:
                        if b[k]:
                            book.__dict__[k] = datetime.datetime.strptime(b[k][0:19], "%Y-%m-%d %H:%M:%S")
                    else:
                        book.__dict__[k] = b[k]

                else:
                    authorList = list()
                    for a in b[k]:
                        author = Author()
                        for aKey in a:
                            author.__dict__[aKey] = a[aKey]
                            authorList.append(author)
            book.bookPath = one

            authorBookLink = AuthorBookLink()
            authorBookLink.author = author
            authorBookLink.book = book
            self.session.add(authorBookLink)

        self.session.commit()
        print 'data loaded'

    def saveAuthorBookLink(self, authorBookLink):
        self.session.add(authorBookLink)
        self.session.commit()

    def saveBook(self, book):
        self.session.add(book)
        self.session.commit()
        self.session.flush()

    def findAllBook(self):
        bs = self.session.query(Book).all()
        print 'completed'
        return bs
    def findBookByIsbn(self, isbn_13):
        bs = self.session.query(Book).filter(Book.isbn_13 == isbn_13).first()
        return bs
    def findBookByNextMaxId(self, bookId):
        bs = self.session.query(Book).filter(Book.id > bookId).order_by(Book.id.asc()).first()
        print 'completed'
        return bs
    def findBookByPreviousMaxId(self, bookId):           
        bs = self.session.query(Book).filter(Book.id < bookId).order_by(Book.id.desc()).first()
        print 'completed'
        return bs        
    def removeBook(self, book=None):
        print 'removeBook'
        try:
            if book:
                path = book.bookPath
                query = self.session.query(Book).filter(Book.id == book.id)
                books = query.all()
                book = books[0]
                
                author_id_lst = []
                for author in book.authors:
                    author_id_lst.append(author.id)
                
                self.session.delete(book)
                self.session.commit()
                self.session.flush()
                
                query = self.session.query(Author).filter(Author.id.in_(author_id_lst))
                authors = query.all()
                for author in authors:
                    self.session.delete(author)
                self.session.commit()
                self.session.flush()                    
                
                path = book.bookPath
                if path and os.path.exists(path):
                    shutil.rmtree(path)
                    print 'deleting path'
        except:
            traceback.print_exc()
            self.session.flush()
            self.session.close()
            



    def findByBookName(self, bookName=None):
        try:
            if bookName:
                query = self.session.query(Book).filter(Book.bookName.ilike('%' + bookName + '%')).order_by(Book.id.desc())
                books = query.all()
                return books
        except:
            traceback.print_exc()


    def findByIsbn_13Name(self, isbn_13=None):
        if isbn_13:
            query = self.session.query(Book).filter(Book.isbn_13.ilike('%' + isbn_13 + '%'))
            books = query.all()
            return books

    def findDuplicateBook(self):
        books = self.session.query(Book).group_by(Book.isbn_13).having(func.count(Book.isbn_13) > 1).order_by(Book.isbn_13.desc())
        return books
    
    def findBookByFileName(self, bookFileName):
        if bookFileName:
            query = self.session.query(Book).filter(Book.bookFileName.ilike('%' + bookFileName + '%'))
            books = query.all()
            return books
    def findBook(self, book=None):
        '''
        This method will find the book in database . It will return true.If book present.

        '''
        books = None
        if book.isbn_13:
            query = self.session.query(Book).filter(Book.isbn_13.ilike('%' + book.isbn_13 + '%'))
            books = query.all()
        if book.bookName:
            query = self.session.query(Book).filter(Book.bookName.ilike('%' + book.bookName + '%'))
            books = query.all()
        return books

    def getMaxBookID(self, book=None):
        '''
        This method will find the book in database . It will return true.If book present.

        '''
        books = None
        maxBookId = self.session.query(func.max(Book.id)).one()
        return maxBookId[0]

if __name__ == '__main__':
#     session = CreateDatabase().creatingDatabase()
#     CreateDatabase().addingData()

#     books = CreateDatabase().findByBookName("java")
    if not os.path.exists(Workspace().path):
        print 'no workspace'
        
    try:
        createdb = CreateDatabase()
        createdb.addingData()
        createdb.findAllBook()
    except:
        print traceback.print_exc()
#     for b in books:
#         print b.isbn_13, b.id


#         createdb.removeBook(b)



    pass
