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
from src.dao.AuthorBookLink import AuthorBookLink
import json
from src.dao.Book import Base, Book
from src.dao.Book import engine
import shutil
import traceback
from src.static.constant import Workspace
import datetime
from src.static.SessionUtil import SingletonSession

from src.audit.singletonLoggerLogging import Logger

logger = Logger(__name__)
logger.info('BookDao logger init')
#  def getSession(self):
logger.info('getcwd-->' + os.getcwd())
logger.info('os.name-->' + os.name)
logger.info('sys.platform-->' + sys.platform)

if os.path.exists(Workspace().libraryPath):
    os.chdir(Workspace().libraryPath)
    listOfDir = os.listdir(Workspace().libraryPath)
    
 
class CreateDatabase():

    def __init__(self):
        '''
        Creating database for library.
        '''
        self.engine = create_engine('sqlite:///' + Workspace().libraryPath + os.sep + '_opal.sqlite', echo=False)
        Session = sessionmaker(autoflush=True, autocommit=False, bind=self.engine)
        self.session = SingletonSession().session
        
        if not os.path.exists(Workspace().libraryPath):
            os.mkdir(Workspace().libraryPath)
        os.chdir(Workspace().libraryPath)
        

    def creatingDatabase(self):
        os.chdir(Workspace().libraryPath)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def addSingleBookData(self, dirName):
        '''
        Using this method you can update single book info into database.
        '''
        try:
            single = {}
            duplicate = {}
            libraryPath = Workspace().libraryPath
            os.chdir(libraryPath)
            duplicateBooks = list()
            addDatabase = True
            b = self.readJsonFile(dirName=dirName)
            book = self.createBookFromJson(bookJson=b)
            book.bookPath = os.path.join(libraryPath , dirName)
            if book.isbn_13: 
                if not single.has_key(book.isbn_13):
                    single[book.isbn_13] = book
                    
                else:
                    duplicate[book.isbn_13] = book
                    addDatabase = False
                    duplicateBooks.append(duplicate)
            if addDatabase:
                self.session.add(book)
            self.session.commit()
        except:
            traceback.print_exc()
            self.session.rollback();
            
            
    def addingData(self):

        directory_name = Workspace().libraryPath
        os.chdir(directory_name)
        listOfDir = list()
#         listOfDir = [ name for name in os.listdir(directory_name) if os.path.isdir(os.path.join(directory_name, name)) ]
        for name in os.listdir(directory_name):
            if os.path.isdir(os.path.join(directory_name, name)) :
                try:
                    if int(name):
                        listOfDir.append(name)
                except Exception as e:
                    pass
        if listOfDir:
            listOfDir.sort(key=int)
        one = ''
       
        try:    
            single = {}
            duplicate = {}
            self.duplicateBooks = list()
            for dirName in listOfDir:
                addDatabase = True
                b = self.readJsonFile(dirName=dirName)
                book = self.createBookFromJson(bookJson=b)
                book.bookPath = os.path.join(directory_name , dirName)
                if book.isbn_13: 
                    if not single.has_key(book.isbn_13):
                        single[book.isbn_13] = book
                        
                    else:
                        duplicate[book.isbn_13] = book
                        addDatabase = False
                        self.duplicateBooks.append(duplicate)
#                 print single
                if addDatabase:
                    self.session.add(book)
            self.session.commit()
            print self.duplicateBooks
    
        except:
#             print duplicate
            traceback.print_exc()
            self.session.rollback();
        print 'data loaded'
    
    def createBookFromJson(self, bookJson=None):
        book = Book()
        for k in bookJson:
            if not isinstance(bookJson[k], list):
                if k in ['publishedOn', 'createdOn']:
                    if bookJson[k]:
                        book.__dict__[k] = datetime.datetime.strptime(bookJson[k][0:19], "%Y-%m-%d %H:%M:%S")
                else:
                    book.__dict__[k] = bookJson[k]

            else:
                authorList = list()
                for a in bookJson[k]:
                    author = Author()
                    for aKey in a:
                        author.__dict__[aKey] = a[aKey]
                        authorList.append(author)
                book.authors = authorList
        return book
    
    def readJsonFile(self, dirName=None):
#         print 'readJsonFile----->', os.path.join(Workspace().libraryPath, dirName , 'book.json')
        try:
            if os.path.exists(os.path.join(Workspace().libraryPath, dirName , 'book.json')):
                bookJsonFile = open(os.path.join(Workspace().libraryPath, dirName , 'book.json'), 'r')
            else:
                os.removedirs(os.path.join(Workspace().libraryPath, dirName)) 
        except Exception as e:
            print e
            print os.path.join(Workspace().libraryPath, dirName)
            
            
        
        rep = ''
        for line in bookJsonFile:
            rep = rep + line
        bookJsonFile.close
        b = None
        try:
            b = json.loads(rep)
        except:
            traceback.print_exc()
#             print rep
        return b

    def saveAuthorBookLink(self, authorBookLink):
        self.session.add(authorBookLink)
        self.session.commit()

    def saveBook(self, book):
        self.session.add(book)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def countAllBooks(self):
        bookCount = 0
        try:
            bookCount = self.session.query(Book).count()
        except:
            pass
        return bookCount
    
    def findAllBook(self, pageSize=None):
#         bs = self.session.query(Book).all()
        bs = self.pagination(pageSize, 0)
        print 'completed'
        return bs
    
    def pagination(self, limit, offset):
        if limit:
            query = self.session.query(Book).limit(limit).offset(offset)
        else:
            query = self.session.query(Book)
        bs = None
        try:    
            bs = query.all()
        except:
            pass
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
        '''
        This method removes entry from database. 
        '''
        isBookDeleted = False
        try:
            if book:
                query = self.session.query(Book).filter(Book.id == book.id)
                book = query.first()
#                 print book
#                 book = books[0]
                
                author_id_lst = []
                for author in book.authors:
                    author_id_lst.append(author.id)
                    self.session.delete(author)
                    
#                 query = self.session.query(AuthorBookLink).filter(AuthorBookLink.bookId == book.id)
#                 authorBookLinks = query.all()
                self.session.delete(book)
#                 for authorBook in authorBookLinks:
#                     self.session.delete(authorBook)
                
#                 query = self.session.query(Author).filter(Author.id.in_(author_id_lst))
#                 authors = query.all()
#                 for author in authors:
#                     self.session.delete(author)
#                 self.session.delete(book)
                self.session.commit()
                
                
#                 path = book.bookPath
#                 if path and os.path.exists(path):
#                     shutil.rmtree(path)
#                     print 'deleting path'
                isBookDeleted = True
        except:
            traceback.print_exc()
            self.session.flush()
            self.session.close()
            isBookDeleted = False
            

        return isBookDeleted

    def findByBookName(self, bookName=None):
        '''
        This method provide search of book name IGNORECASE .
        '''
        try:
            if bookName:
                query = self.session.query(Book).filter(func.lower(Book.bookName) == func.lower(bookName)).order_by(Book.id.desc())
                books = query.all()
                return books
        except:
            traceback.print_exc()
            
    def findBySimlarBookName(self, bookName=None):
        '''
        This method provide search of book name IGNORECASE and similar result like.
        '''
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
#         maxBookId = self.session.query(func.max(Book.id)).one()
        length = len(Workspace().libraryPath) + 2
        print length
        sql = 'select max(substr(book_path,' + str(length) + '), id) from book order by id desc'
        print 'getMaxBookID----sql: > ', sql
        maxBookId = self.session.execute(sql).first()
        if maxBookId == None:
            maxBookId = [0]
        print int(maxBookId[0])
        return int(maxBookId[0])

if __name__ == '__main__':
#     session = CreateDatabase().creatingDatabase()
#     CreateDatabase().addingData()

#     books = CreateDatabase().findByBookName("java")
    if not os.path.exists(Workspace().libraryPath):
        print 'no workspace'
        
    try:
        createdb = CreateDatabase()
#         createdb.creatingDatabase()
#         createdb.addingData()
        x = createdb.getMaxBookID()
        page = createdb.paginatiion(10, 10)
        print page
#         createdb.findAllBook()
    except:
        print traceback.print_exc()
#     for b in books:
#         print b.isbn_13, b.id


#         createdb.removeBook(b)



    pass
