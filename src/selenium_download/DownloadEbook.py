'''
Created on 22-Mar-2016

@author: vijay
'''
import urllib2
from bs4 import BeautifulSoup
import json
import os
import logging
import time
import urllib
from selenium import webdriver
from src.static.constant import Workspace
from datetime import datetime
from src.logic.search_book import FindingBook
import threading
from src.dao.BookDao import CreateDatabase
import thread
import traceback
from test.dao.missing import Missing
import logging

logger = logging.getLogger('extensive')




# directory_name = '/docs/selenium/books'
# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='myapp.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)


class Book(json.JSONEncoder):
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
        self.fileSize = fileSize
        self.bookFormat = bookFormat
        self.subTitle = bookSubTitle
        self.itEbookUrlNumber = None

    def __str__(self):
        rep = self.name + self.publisher + self.author + self.isbn + self.datePublished + self.numberOfPages + self.inLanguage + self.fileSize + self.bookFormat
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
        
class DownloadItEbook(threading.Thread):
    '''
    This class will download books from itebook.info
    '''


    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        '''
        Constructor, setting location of downloaded book.
        '''
        super(DownloadItEbook, self).__init__(group=group, target=target, name=name, verbose=verbose)
        
        self.args = args
        self.kwargs = kwargs
        self.directory_name = Workspace().libraryPath
        self.createDatabase = CreateDatabase()   
        pass

    def run(self):
        print ('running with %s and %s', self.args, self.kwargs)
        return
    
    def getUrl(self, baseUrl, number):
        '''this method will find and constuct all url of url given'''
        return baseUrl + '/book/' + str(number)

    def findBookDetail(self, baseUrl, number):
        ''' This method will download book cover.
         It will provide book object.'''
        url = self.getUrl(baseUrl, number)
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
        book = Book()
        book.authors.append(Author(soup.find_all(itemprop="author")[0].text))
        book.isbn_13 = soup.find_all(itemprop="isbn")[0].text
        book.bookName = soup.find_all(itemprop="name")[0].text
        book.publisher = soup.find_all(itemprop="publisher")[0].text
        
        try:
            date = datetime.strptime(str(soup.find_all(itemprop="datePublished")[0].text) , '%Y')
        except:
            date = datetime.now()
        book.publishedOn = date
        
        book.numberOfPages = soup.find_all(itemprop="numberOfPages")[0].text
        book.inLanguage = soup.find_all(itemprop="inLanguage")[0].text
        book.bookFormat = soup.find_all(itemprop="bookFormat")[0].text
        book.bookDescription = soup.find_all(itemprop="description")[0].text
        book.bookImgName = (soup.find_all(itemprop="image")[0]).get('src')
        try:
            book.subTitle = soup.h3.text
        except:
            traceback.print_exc()
        book.fileSize = soup.find_all('table')[3].find_all('tr')[7].find_all('td')[1].find_all('b')[0].text
#         book.fileSize=

#         .top > div:nth-child(2) > h3:nth-child(2)


        for link in soup.find_all('a'):
            if link.get('href').startswith('http://filepi.com'):
                book.name = link.text
                break
        return book

    def getMaxBookID(self):
        maxBookId = self.createDatabase.getMaxBookID()
        if not maxBookId:
            maxBookId = 0        
        return maxBookId
    def downloadDir(self):
        '''
        This function will create directory to download book.
        @param number:it takes database maxId+1 to create new directory . 
        '''
        directory_name = os.path.join(self.directory_name, str(self.getMaxBookID() + 1))
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        return directory_name
        
        
    def firefoxDownloadJob(self, book, baseUrl, number):
        '''The function of this method is to download link of given URL.'''
        directory_name = self.downloadDir()
        # Creating Actual URL
        url = self.getUrl(baseUrl, number)
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        lsFiles = []
        # Checking if there are three files in this URL.
        # Creating a list of absolute files.
        if 3 == len(os.listdir(directory_name)) :
            for sName in os.listdir(directory_name):
                if os.path.isfile(os.path.join(directory_name, sName)):
                    lsFiles.append(sName)

        # Checking if there are more than 3 files in the directory location.
        # Removing all the files from direcotry.
        elif 3 != len(os.listdir(directory_name)):
            for sName in os.listdir(directory_name):
                os.remove(directory_name + '/' + sName)

            imageUrl = url + book.bookImgName
            subUrl = book.bookImgName
            imageFileName = subUrl.split('/')[-1:][0]
            logging.info(imageUrl)

            # Downloading book cover
            bookImagePath = os.path.join(directory_name, subUrl.split('/')[-1:][0])
            urllib.urlretrieve(baseUrl + book.bookImgName, bookImagePath)
            book.bookImgName = imageFileName
            f = open(os.path.join(directory_name, 'book.json'), 'w')
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
            f.write(json.dumps(row2dict, sort_keys=False, indent=4))
            f.close()

            fp = webdriver.FirefoxProfile()


            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference('browser.download.manager.showWhenStarting', False)
            fp.set_preference('browser.download.manager.focusWhenStarting', False)
            fp.set_preference("browser.download.dir", directory_name)
            fp.set_preference("browser.download.manager.scanWhenDone", False)
            fp.set_preference("browser.download.manager.useWindow", False)
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            fp.update_preferences()
            driver = webdriver.Firefox(firefox_profile=fp)
            # driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]/img")
            driver.get(url)
            efd_link = driver.find_element_by_link_text(book.name)
            book.fileSize = driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td[2]/table/tbody/tr[8]/td[2]/b").text
            book.bookFormat = driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td[2]/table/tbody/tr[9]/td[2]/b").text
            efd_link.click()
            flag = True
            while(flag):
                # # checking part file
                time.sleep(10)
                lst = []
                files = []
                for sName in os.listdir(directory_name):
                    if os.path.isfile(os.path.join(directory_name, sName)):
                        logging.info(sName.split('.')[-1:][0])
                        lst.append(sName.split('.')[-1:][0])
                        files.append(os.path.join(directory_name, sName))
                print lst
                if 'part' not in lst:
                    logging.info("flag :" + str(flag))
                    flag = False
                    time.sleep(10)
                    driver.close()
                else:
                    # print files
#                     if not self.isBookDownloading(files):
#                         driver.close()
                    pass

    def writeJsonToDir(self, bookPath=None, book=None):
        '''
        this function will write json file to given dir.
        '''
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
            f.write(json.dumps(row2dict, sort_keys=False, indent=4))
            f.close()     
        except:
            traceback.print_exc()   
        
    def isBookDownloading(self, files):
        ''' This method will inform that book is getting downloading or not.'''
        # time.sleep(2)
        dic_files = {}
        time_dic_files = {}
        i = 1
        checkFlagForSize = True
        isDownloading = True
        for fl in files:
            dic_files[fl] = str(os.stat(fl).st_size)
        while(checkFlagForSize):

            time_dic_files[i] = dic_files
            i = i + 1
            if i > 4:
                size = set()
                for k in time_dic_files[i - 1]:
                    if 'part' in k:
                        size.add(time_dic_files[i - 1][k])
                for k in time_dic_files[i - 2]:
                    if 'part' in k:
                        size.add(time_dic_files[i - 2][k])
                for k in time_dic_files[i - 3]:
                    if 'part' in k:
                        size.add(time_dic_files[i - 3][k])
#                 print len(list(size))
                if len(list(size)) > 1:
                    isDownloading = False
            checkFlagForSize = False
        logging.info('isDownloading:')
        return isDownloading


    def startDownload(self):
        baseUrl = 'http://it-ebooks.info'
        miss = Missing()
#         lst = miss.missingNumbers()
        lst = [1464348534, 7102]
        for number in lst:
            print number
#         for number in range(6998, 0, -1):
            itebook = DownloadItEbook()
            url = itebook.getUrl(baseUrl, number)
            a = urllib2.urlopen(url)
            strig = a.geturl()
            if  '404' != strig[-4:-1]:
                book = itebook.findBookDetail(baseUrl, number)
                # Is this book already availble (downloaded)
                # check book whethere it is existing in database.
                bs = FindingBook().findBookByIsbn(isbn_13=book.isbn_13)
                if bs:
                    print 'this books is already present.', book.isbn_13, book.bookName
                else:
                    try:
                        self.firefoxDownloadJob(book, baseUrl, number)
                        self.updateDatabase()
                    except:
                        print number, baseUrl
                        traceback.print_exc()
#                 try:
#                     thread.start_new_thread( self.updateDatabase, ())
#                 except:
#                     traceback.print_exc()
                    
#                 logging.info("checking  Is this book already availble (downloaded)" + book.bookName)
    def updateDatabase(self):
        self.createDatabase.creatingDatabase()  
        self.createDatabase.addingData()        
    
    def updateBooksMetadata(self):
        miss = Missing()
        listOfDir = miss.availableNumbers()
        listOfDir=listOfDir[1391:]
        baseUrl = 'http://it-ebooks.info'
        for number in listOfDir:
            logger.debug( 'updating book number: %s',number)
#             url = self.getUrl(baseUrl, number)
#             a = urllib2.urlopen(url)
#             strig = a.geturl()
#             if  '404' != strig[-4:-1]:
    #             number=7102
        #         genUrl=self.downloadItEbook.getUrl(baseUrl, number)
            try:
                book=self.findBookDetail(baseUrl, number)
                book.itEbookUrlNumber=number
                subUrl = book.bookImgName
                imageFileName = subUrl.split('/')[-1:][0]
                book.bookImgName=imageFileName
                bookPath=os.path.join(Workspace().libraryPath,number)
                self.writeJsonToDir(bookPath, book)
            except:
                traceback.print_exc()
        
if __name__ == "__main__":
    print ' started'
#     for i in range(3):
#         print i
#         t = DownloadItEbook(args=(i,), kwargs={'a':1, 'b':2})
#         t.start()
    it = DownloadItEbook()
#     it.updateBooksMetadata()
    it.startDownload()
    print ' completed'
