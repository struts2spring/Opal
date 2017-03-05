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
        AQGPK3595C
        '''
#         url = 'http://dl.fullcirclemagazine.org/issue1_en.pdf'
#         'http://dl.fullcirclemagazine.org/issue3_en.pdf'
        directory_name = self.createDownloadDir()
        bookImagePath = os.path.join(directory_name, book.bookImgName)
        os.chdir(directory_name)
        r = requests.get(url, headers=self.header_info, timeout=30)
        if r.status_code == 200:
            print r.status_code, url
            print '------->', int(r.headers["content-length"]) / 1000000
            book.fileSize = str(round(int(r.headers["content-length"]) / 1000000 , 2)) + ' MB'
            self.writeJsonToDir(directory_name, book)
            self.downloadBookImage(bookImagePath, self.imageUrl)
#             r = requests.get(bookUrl, headers=self.header_info, timeout=30)
            print '--------------->', r.url
            bookPath = os.path.join(directory_name, url.split('/')[-1])
            print bookPath
            with open(bookPath, 'wb') as bookFile:
                
                bookFile.write(r.content)
            self.updateDatabase(directory_name)
        return r.status_code, directory_name  
    
    def createBookDetail(self, bookName=None):
        book = Book()   
        book.bookName = "Full Circle "+ bookName
        book.bookFormat = 'pdf'
        book.tag = 'Technology'
        book.inLanguage = 'English'
        book.subTitle = 'Magazine'
        book.publisher = "Full Circle"
        book.bookImgName = bookName + '.jpg'
        book.hasCover = 'Yes'
        book.hasCode = 'No'
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
        print imageUrl
        head, data = imageUrl.split(',', 1)
        bits = head.split(';')
        mime_type = bits[0] if bits[0] else 'text/plain'
        charset, b64 = 'ASCII', False
        for bit in bits:
            if bit.startswith('charset='):
                charset = bit[8:]
            elif bit == 'base64':
                b64 = True
        
        # Do something smart with charset and b64 instead of assuming
        plaindata = data.decode("base64")
        
        # Do something smart with mime_type
        with open(bookImagePath, 'wb') as f:
            f.write(plaindata)

        print 'write image complete'
#         from PIL import Image   
#         from StringIO import StringIO
#         r = requests.get(imageUrl, headers=self.header_info, timeout=30)
#         print '--------------->', r.url
#         with open(bookImagePath, 'wb') as imageFile:
#             imageFile.write(r.content)    


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
            os.makedirs(directory_name,755)
            os.chdir(directory_name)
        return directory_name
    
    def getMaxBookID(self):
        maxBookId = self.createDatabase.getMaxBookID()
        if not maxBookId:
            maxBookId = 0        
        return maxBookId
    
    
    def getImageUrl(self, completeUrl, issueCount):
        print completeUrl
        imageUrl = None
        r = requests.get(completeUrl, headers=self.header_info, timeout=30)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
#             print soup
            alt = soup.find(class_='issuetable').find('img')['alt']
            if alt == 'Cover for Issue '+issueCount+' in English':
                imageUrl = soup.find(class_='issuetable').find('img')['src']
                print imageUrl
        return imageUrl
    
    def startDownload(self):
        logic = True
        i = 1
        while logic:
            pdfUrl = 'http://dl.fullcirclemagazine.org/issue' + str(i) + '_en.pdf'
            completeUrl = 'http://fullcirclemagazine.org/issue-' + str(i) + '/'
            if not self.isIssuePresent(str(i)):
                self.imageUrl = self.getImageUrl(completeUrl,str(i))
                book = self.createBookDetail('Issue ' + str(i))
                status_code, directory_name = self.downloadFullCircleMagazine(book=book, url=pdfUrl)
                print completeUrl, status_code
                if status_code != 200:
                    logic = False
            i = i + 1
    
    
    def isIssuePresent(self, issue=None):
        isBookPresent = False
        bookName="Full Circle Issue " + issue
        book = self.createDatabase.findByBookName(bookName)
        if book:
            isBookPresent = True
        return isBookPresent

    def getIssueDetail(self):
        url='https://wiki.ubuntu.com/UbuntuMagazine/FullIssueIndex'
        r = requests.get(url, headers=self.header_info, timeout=30)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml") 
            tables=soup.findAll('table')
            for table in tables:
                print table
            
    
if __name__ == '__main__':
    print 'hi'
    fullCircleMagazine = FullCircleMagazine()
#     fullCircleMagazine.getIssueDetail()
    fullCircleMagazine.startDownload()
    # bookImagePath='/docs/new/1'

    # "data:image/jpeg;base64,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""
    # base64_image_str = base64_image_str[base64_image_str.find(",")+1:]
    # fullCircleMagazine.downloadBookImage(bookImagePath, base64_image_str)
    pass
