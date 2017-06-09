import os
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
# from src.dao.Book import Base
from src.static.constant import Workspace
import traceback
from sqlalchemy.ext.declarative import  declarative_base


from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, \
    Column, Integer, String, Column, Integer, String

import logging

logger = logging.getLogger('extensive')



Base = declarative_base()
databaseFileName = '_opal_online.sqlite'
onlineDatabaseUrl = 'sqlite:///' + Workspace().searchedPath + os.sep + databaseFileName

class OnlineDatabase():


    def __init__(self):
        '''
        Creating database for library.
        '''
        logger.debug('OnlineDatabase')
        self.engine = create_engine(onlineDatabaseUrl, echo=True)
        Session = sessionmaker(autoflush=True, autocommit=False, bind=self.engine)
        self.session = OnlineSingletonSession().session
        
        if not os.path.exists(Workspace().searchedPath):
            os.mkdir(Workspace().searched)
        os.chdir(Workspace().searchedPath)
        

    def creatingDatabase(self):
        logger.debug('creatingDatabase')
        os.chdir(Workspace().libraryPath)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)


    def addingData(self, listOfBook=None):
        logger.debug('addingData')
        try:
            for b in listOfBook:
                
                book = OnlineBook()
                book = self.copyBookProperty(b, book)
                logger.debug('source:', b)
                logger.debug('destination:', book)
                databaseBook = self.session.query(OnlineBook).filter(OnlineBook.isbn_13 == book.isbn_13).first()
                if databaseBook is None:
                    self.session.add(book)
        except Exception as e:
            self.session.flush()
            logger.error(e, exc_info=True)
            traceback.print_exc()
        self.session.commit()

    def copyBookProperty(self, source, destination):
        logger.debug('copyBookProperty')
        for sKey, sValue in source.__dict__.iteritems():
            print sKey, sValue
            if sKey == 'rating':
                if sValue != None:
                    destination.__dict__['customerReview'] = sValue.strip()
            elif sKey not in ['id']:
                if sValue != None:
                    destination.__dict__[sKey] = sValue.strip()
#             for dKey in destination.__dict__.iterkeys():
#                 if dKey == sKey:
            
#         destination.__dict__.update(source.__dict__)
        return destination
    
    def findIsbnList(self, isbnList=None):
        '''
        Function return list of books of given isbnList.
        '''
        print 'findBookInfo'
        result = None
        if isbnList:
            query = self.session.query(OnlineBook.isbn_10).filter(OnlineBook.isbn_10.in_(isbnList))
            result = query.all()
            
        return result
    
    def findBookInfo(self, isbnList=None):
        '''
        Function return list of books of given isbnList.
        '''
        print 'findBookInfo'
        result = None
        if isbnList:
            query = self.session.query(OnlineBook).filter(OnlineBook.isbn_10.in_(isbnList))
            result = query.all()
            
        return result


class OnlineSingletonSession(object):
    
    class __OnlineSingletonSession:
        def __init__(self):
            self.createSession()
        def __str__(self):
            return repr(self) + self.val
    
    
        def createSession(self):
            engine = create_engine(onlineDatabaseUrl, echo=True)
            Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
            self.session = Session()
            database_fileName = os.path.join(Workspace().searchedPath , databaseFileName)
            if not os.path.exists(database_fileName) or os.path.getsize(database_fileName) == 0:
                if not os.path.exists(Workspace().searchedPath):
                    os.mkdir(Workspace().searchedPath)
                os.chdir(Workspace().searchedPath)
    #             print '---------------------------',os.path.getsize(database_fileName)
    #             self.creatingDatabase()
                print Base.metadata.drop_all(engine)
                print Base.metadata.create_all(engine)
        
        
    
    instance = None
    def __new__(cls):  # __new__ always a classmethod
        if not OnlineSingletonSession.instance:
            OnlineSingletonSession.instance = OnlineSingletonSession.__OnlineSingletonSession()
        return OnlineSingletonSession.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)





class OnlineBook(Base):
    __tablename__ = 'book'
    """A Book class is an entity having database table."""
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    searchedText = Column('search_text', String)  # key with which this book has been searched
    source = Column('source', String)
    bookName = Column('book_name', String(46), nullable=False)  # bookName
    subTitle = Column('sub_title', String)  # Title
    isbn_10 = Column(String)  # isbn_10
    isbn_13 = Column(String, unique=True)  # isbn_13
    asin=Column(String, unique=True)
    series = Column(String)  # series
    dimension = Column(String)  # dimension
    customerReview = Column('customer_review', String)  # customerReview
    bookDescription = Column('book_description', String)  # bookDescription
    editionNo = Column('edition_no', String)  # editionNo
    publisher = Column(String)  # publisher
    bookFormat = Column("book_format", String)  # bookFormat
    fileSize = Column('file_size', String)  # fileSize
    numberOfPages = Column('number_of_pages', Integer)  # numberOfPages
    inLanguage = Column('in_language', String)  # inLanguage
#     publishedOn = Column('published_on', DateTime, default=func.now())
    hasCover = Column('has_cover', String)  # hasCover
    hasCode = Column('has_code', String)  # hasCode
    bookPath = Column('book_path', String)  # bookPath
    rating = Column('rating', String)  # rating
    uuid = Column('uuid', String)  # uuid
    tag = Column('tag', String)  # a comma separated list of subjects
    bookFileName = Column('book_file_name', String)
    bookImgName = Column('book_img_name', String)  # a comma separated list of images for the book
    wishListed = Column('wish_listed', String)  # this is an indicator that book is not available in workspace.
    itEbookUrlNumber = Column(String)
    aboutAuthor = Column('about_author', String)
#     createdOn = Column('created_on', DateTime, default=func.now())


if __name__ == '__main__':
#     session = CreateDatabase().creatingDatabase()
#     CreateDatabase().addingData()

#     books = CreateDatabase().findByBookName("java")
    if not os.path.exists(Workspace().searchedPath):
        print 'no workspace'
        
    try:    
        createdb = OnlineDatabase()
        createdb.creatingDatabase()
        createdb.addingData()
#         createdb.findAllBook()
    except:
        print traceback.print_exc()
