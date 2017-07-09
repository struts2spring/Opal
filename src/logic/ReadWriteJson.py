'''
Created on 12-Apr-2016

@author: vijay
'''
import os
import json
import datetime
from src.static.constant import Workspace
import logging

logger = logging.getLogger('extensive')

class Book(json.JSONEncoder):
    '''
    This class has been used to write json object of book.
    '''
    def __init__(self, name=None, publisher=None, authors=None, isbn=None, datePublished=None, numberOfPages=None,
                 inLanguage=None, fileSize=None, bookFormat=None, bookDescription=None, image=None, bookSubTitle=None):
        '''
        Constructor
        '''
        self.bookName = name
        self.publisher = publisher
        
        self.authors = list()
        
        self.isbn_13 = isbn
        self.publishedOn = datePublished
        self.numberOfPages = numberOfPages
        self.inLanguage = inLanguage
        self.bookFormat = list()
        self.subTitle = bookSubTitle
        self.itEbookUrlNumber = None

    def __str__(self):
        rep = self.name + self.publisher + self.author + self.isbn + self.datePublished + self.numberOfPages + self.inLanguage + self.fileSize + self.bookFormat
        return rep
    def __eq__(self, other):
        return self.bookName == other.bookName \
            and self.isbn_13 == other.isbn_13
class Author(json.JSONEncoder):
    '''
    This class has been used to write json object of author of book.
    '''
    def __init__(self, authorName='unknown', aboutAuthor=None):
        '''
        Constructor
        '''
        self.authorName = authorName
        self.aboutAuthor = aboutAuthor
        
    def __str__(self):
        rep = self.authorName 
        return rep
    
    def __eq__(self, other):
        return self.authorName == other.authorName and self.aboutAuthor == other.aboutAuthor

class ReadWriteJsonInfo(object):
    '''
    This is the class used to read and write json file in dir.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass

    def readJsonFromDir(self, dirName=None):
        '''
        This method read the json file from workspace and return book object.
        @param dirName: this is directory name.
        '''
        logger.debug('readJsonFromDir: %s',dirName)
        bookJsonFile = open(os.path.join(Workspace().libraryPath, dirName , 'book.json'), 'r')

        rep = ''
        for line in bookJsonFile:
            rep = rep + line
        bookJsonFile.close
        b=None
        try:
            b = json.loads(rep)
        except Exception as e:
            logger.error(e, exc_info=True)
        return b         
    
 
    
    def writeJsonToDir(self, bookPath=None, book=None):
        '''
        this function will write json file to given dir.
        @param bookPath: path of book : Book.
        @param book: book object :Book
        '''
        logger.info('writeJsonToDir')
        try:
            
            f = open(os.path.join(bookPath, 'book.json'), 'w')
            row2dict = book.__dict__
            authors = []
            if row2dict.has_key('publishedOn'):
                if type(row2dict['publishedOn']) == datetime or type(row2dict['publishedOn']) == datetime.datetime:
#                     row2dict['publishedOn'] = str(row2dict['publishedOn'])
                    
#                     row2dict['publishedOn'] = str("%Y-%m-%d %H:%M:%S".format(row2dict['publishedOn']))
                    row2dict['publishedOn'] = str(row2dict['publishedOn'])
            if row2dict.has_key('createdOn'):
                if type(row2dict['createdOn']) == datetime or type(row2dict['createdOn']) == datetime.datetime:
                    row2dict['createdOn'] = str(row2dict['createdOn'])
#                 row2dict['publishedOn']=datetime.datetime.strptime(row2dict['publishedOn'][0:19], "%Y-%m-%d %H:%M:%S")
            for a in row2dict['authors']:
                author = {}
                if type(a) == str:
                    author['authorName'] = a
                else:
                    author = a.__dict__
                if author.has_key('_sa_instance_state'):
                    del author['_sa_instance_state']
                if author.has_key('book_assoc'):
                    del author['book_assoc']
                    
                authors.append(author)
                
            if row2dict.has_key('_sa_instance_state'):
                del row2dict['_sa_instance_state']
            if row2dict.has_key('authors'):   
                del row2dict['authors']
            if row2dict.has_key('book_assoc'):  
                del row2dict['book_assoc']  
            if row2dict.has_key('__len__'):  
                del row2dict['__len__']  
            if row2dict.has_key('id'):  
                del row2dict['id']  
                  
            row2dict['authors'] = authors
            f.write(json.dumps(row2dict, sort_keys=True, indent=4, default=str))
            f.close()     
        except Exception as e:
            logger.error(e, exc_info=True)
            
if __name__=='__main__':
    pass
        