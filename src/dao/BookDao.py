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

#  def getSession(self):
print '3--->', os.getcwd(), os.name, sys.platform
if sys.platform=='win32':
#     Workspace().path='e:\\docs\\books'  
    Workspace().path='C:\\new'  
else:  
    Workspace().path='/docs/books'
os.chdir(Workspace().path)
listOfDir = os.listdir(Workspace().path)




engine = create_engine('sqlite:///'+Workspace().path+os.sep+'_opal.sqlite', echo=True)
Session = sessionmaker(autoflush=True, autocommit=False, bind=engine)
session = Session()

# os.chdir(Workspace().path)
# if len(listOfDir)>0:
#     print len(listOfDir)
#     for sName in listOfDir:
#         pass
# else:
#     os.chdir(Workspace().path)
#     print '3--->', os.getcwd()
#     session = CreateDatabase().creatingDatabase()
#     CreateDatabase().addingData()

#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)

class CreateDatabase():




    def creatingDatabase(self):
        os.chdir(Workspace().path)
        print Base.metadata.drop_all(engine)
        print Base.metadata.create_all(engine)
        pass
#         self.getSession()


    def addingData(self):
#         session=self.getSession()
#         directory_name = '/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books'
        directory_name = Workspace().path
#         directory_name = os.getcwd()
        os.chdir(directory_name)
        listOfDir = [ name for name in os.listdir(directory_name) if os.path.isdir(os.path.join(directory_name, name)) ]
        if listOfDir:
            listOfDir.sort(key=int)
        one = ''
        # create a Session
#         sess = session()
        session = Session()
        for sName in listOfDir:
            one = os.path.join(directory_name , sName)
            # print one
            file = open(os.path.join(one ,'book.json'), 'r')

            rep = ''
            for line in file:
                rep = rep + line
            file.close
            # print str(rep)
            b = json.loads(rep)

            book = Book(bookName=b["name"], fileSize=b["fileSize"], hasCover='Y', bookPath=one , bookDescription=b["bookDescription"], publisher=b["publisher"], isbn_13=b["isbn"], numberOfPages=b["numberOfPages"], bookFormat=b["bookFormat"], inLanguage=b["inLanguage"])
            # book.bookName='one'

            author = Author(authorName=b["author"])
            authorList = list()
            authorList.append(author)
            book.authors = authorList

            authorBookLink = AuthorBookLink()
            authorBookLink.author = author
            authorBookLink.book = book
            session.add(authorBookLink)

        session.commit()
        print 'data loaded'

    def findAllBook(self):
#         session=self.getSession()
        bs = session.query(Book).all()
#         for b in bs:
#             print b

        print 'completed'
        return bs

    def removeBook(self, book=None):
#         session=self.getSession()
        try:
            if book:

    #             for author in book.authors:
    #                 session.delete(author)

                author_book = session.query(AuthorBookLink).filter(AuthorBookLink.book == book).all()
                if author_book and len(author_book) > 0:
                    print author_book[0].bookId
                    session.delete(author_book[0])
                for author in book.authors:
                    session.delete(author)

#                 session.delete(book)
#                 session.commit()

                path = book.bookPath
                if path and os.path.exists(path):
                    shutil.rmtree(path)
                    print 'deleting path'
        except:
            traceback.print_exc()



    def findByBookName(self, bookName=None):
        try:
            if bookName:
                query = session.query(Book).filter(Book.bookName.ilike('%' + bookName + '%')).order_by(Book.id.desc())
                books = query.all()
                return books
        except:
            traceback.print_exc()


    def findByIsbn_13Name(self, isbn_13=None):
        if isbn_13:
            query = session.query(Book).filter(Book.isbn_13.ilike('%' + isbn_13 + '%'))
            books = query.all()
            return books

    def findDuplicateBook(self):
#         session=self.getSession()
        books = session.query(Book).group_by(Book.isbn_13).having(func.count(Book.isbn_13) > 1).order_by(Book.isbn_13.desc())
#         print len(bs)
#         for b in bs:
#             print b.isbn_13,b.id
        return books

    def findBook(self, book=None):
        '''
        This method will find the book in database . It will return true.If book present.

        '''
        books=None
        if book.isbn_13:
            query = session.query(Book).filter(Book.isbn_13.ilike('%' + book.isbn_13 + '%'))
            books = query.all()
        if book.bookName:
            query = session.query(Book).filter(Book.bookName.ilike('%' + book.bookName + '%'))
            books = query.all()

#         uniqueBookSet=set()
#         uniqueBookSet.add(books)
        return books
#         print len(bs)
        pass


if __name__ == '__main__':
#     session = CreateDatabase().creatingDatabase()
#     CreateDatabase().addingData()

#     books = CreateDatabase().findByBookName("java")
#     createdb = CreateDatabase()
#     createdb.addingData()
#     for b in books:
#         print b.isbn_13, b.id


#         createdb.removeBook(b)



    pass
