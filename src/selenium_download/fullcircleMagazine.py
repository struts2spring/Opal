'''
Created on 14-Aug-2016

@author: vijay
'''
import os
import requests
import json
import traceback
import datetime
from src.static.constant import Workspace
from src.dao.BookDao import CreateDatabase
from bs4 import BeautifulSoup


class Book(json.JSONEncoder):
    def __init__(self, name=None, publisher=None, authors=None, isbn_13=None, datePublished=None, numberOfPages=None,
                 inLanguage=None, fileSize=None, bookFormat=None, bookDescription=None, bookImgName=None, bookSubTitle=None,
                 tag=None, subTitle=None):
        '''
        Constructor
        '''
        self.bookName = name
        self.subTitle = subTitle
        self.publisher = publisher
        
        self.authors = list()
        
        self.isbn_13 = isbn_13
        self.publishedOn = datePublished
        self.numberOfPages = numberOfPages
        self.inLanguage = inLanguage
        self.fileSize = fileSize
        self.bookFormat = bookFormat
        self.subTitle = bookSubTitle
        self.bookImgName = bookImgName
        self.tag = tag
        

    def __str__(self):
        rep = self.name + self.publisher + self.author + self.isbn_13 + self.datePublished + self.numberOfPages + self.inLanguage + self.fileSize + self.bookFormat + self.tag
        return rep

class Author(json.JSONEncoder):
    def __init__(self, authorName='unknown'):
        '''
        Constructor
        '''
        self.authorName = authorName
        
    def __str__(self):
        rep = self.authorName 
        return rep

class FullCircleMagazine():
    
    def __init__(self, baseUrl=None):
        self.baseUrl = baseUrl
        self.directory_name = Workspace().libraryPath
        self.createDatabase = CreateDatabase() 
        self.header_info = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'}
        
        # book image url
        self.imageUrl = None
        self.bookUrl = None
        pass
    
    def downloadFullCircleMagazine(self, url, book=None, bookUrl=None):
        '''
        '''
#         url = 'http://dl.fullcirclemagazine.org/issue1_en.pdf'
#         'http://dl.fullcirclemagazine.org/issue3_en.pdf'
        directory_name = self.createDownloadDir()
        r = requests.get(url, headers=self.header_info, timeout=30)
        if r.status_code == 200:
            print r.status_code, url
            
            bookImagePath = os.path.join(directory_name, book.bookImgName)
            self.downloadBookImage(bookImagePath, self.imageUrl)
            self.writeJsonToDir(directory_name, book)
            
            r = requests.get(bookUrl, headers=self.header_info, timeout=30)
            print '--------------->', r.url
            bookPath = os.path.join(directory_name, bookUrl.split('/')[-1])
            with open(bookPath, 'wb') as bookFile:
                bookFile.write(r.content)
            try:
                self.extractRar(directory_name)
            except:
                traceback.print_exc()   
                pass
        return r.status_code, directory_name  
    
    def createBookDetail(self, bookName=None):
        book = Book()   
        book.bookName="Full Circle"+bookName
        book.bookFormat='pdf'
        book.tag='Technology'
        book.inLanguage='English'
        book.subTitle='Magazine'
        book.bookImgName=bookName+'.jpg'
        
        return book
            
    def writeJsonToDir(self, bookPath=None, book=None):
        try:
            f = open(os.path.join(bookPath, 'book.json'), 'w')
            row2dict = book.__dict__
            authors = []
            if type(row2dict['publishedOn']) == datetime:
                row2dict['publishedOn'] = str(row2dict['publishedOn'])
            for a in row2dict['authors']:
                author = {}
                if type(a) == str:
                    author['authorName'] = a
                else:
                    author = a.__dict__
                
                authors.append(author)
            row2dict['authors'] = authors
            if not row2dict['isbn_13'] == None:
                if str(row2dict['isbn_13']).strip() == '':
                    row2dict['isbn_13'] = None
            f.write(json.dumps(row2dict, sort_keys=False, indent=4))
            f.close()     
        except:
            traceback.print_exc()   
            
    def downloadBookImage(self, bookImagePath=None, imageUrl=None):
        '''
        this method will download image from imageUrl location and keep it at bookImagePath
        '''
        from PIL import Image   
        from StringIO import StringIO
        r = requests.get(imageUrl, headers=self.header_info, timeout=30)
        print '--------------->', r.url
        with open(bookImagePath, 'wb') as imageFile:
            imageFile.write(r.content)    


    def updateDatabase(self, directory_name):
#         self.createDatabase.creatingDatabase()  
#         self.createDatabase.addingData() 
        self.createDatabase.addSingleBookData(directory_name)
           
    def isIsbnAvailableInDatabase(self, isbn_13=None):
        isBookPresent = False
        book = self.createDatabase.findByIsbn_13Name(isbn_13)
        if book:
            isBookPresent = True
        return isBookPresent
    
    def isBookNameAvailableInDatabase(self, bookName=None):
        isBookPresent = False
        book = self.createDatabase.findByBookName(bookName)
        if book:
            isBookPresent = True
        return isBookPresent
    
    def createDownloadDir(self):
        '''
        This function will create directory to download book.
        @param number:it takes database maxId+1 to create new directory . 
        '''
        directory_name = os.path.join(self.directory_name, str(self.getMaxBookID() + 1))
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            os.chdir(directory_name)
        return directory_name
    
    def getMaxBookID(self):
        maxBookId = self.createDatabase.getMaxBookID()
        if not maxBookId:
            maxBookId = 0        
        return maxBookId
    
    
    def getImageUrl(self, completeUrl):
        print completeUrl
        imageUrl=None
        r = requests.get(completeUrl, headers=self.header_info, timeout=30)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
            print soup
        return imageUrl
    def startDownload(self):
        logic = True
        i = 1
        while logic:
            pdfUrl = 'http://dl.fullcirclemagazine.org/issue' + str(i) + '_en.pdf'
            completeUrl = 'http://fullcirclemagazine.org/issue-' + str(i) + '/'
            self.getImageUrl(completeUrl)
            book=self.createBookDetail('Issue'+ str(i))
            status_code = self.downloadFullCircleMagazine(book=book, url=pdfUrl)
            print completeUrl, status_code
            if status_code != 200:
                logic = False
            i = i + 1
            
            logic=False
        pass
    
    
    
if __name__ == '__main__':
    print 'hi'
    fullCircleMagazine = FullCircleMagazine()
    fullCircleMagazine.startDownload()
    pass
