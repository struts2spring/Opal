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
    def __init__(self, name=None, publisher=None, authors=None, isbn=None, datePublished=None, numberOfPages=None, inLanguage=None, fileSize=None, bookFormat=None, bookDescription=None, image=None):
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
        
class DownloadItEbook(object):
    '''
    This class will download books from itebook.info
    '''


    def __init__(self):
        '''
        Constructor, setting location of downloaded book.
        '''
        self.directory_name = Workspace().path
        
        pass
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
        
        date = datetime.strptime(str(soup.find_all(itemprop="datePublished")[0].text) , '%Y')
        book.publishedOn = date
        
        book.numberOfPages = soup.find_all(itemprop="numberOfPages")[0].text
        book.inLanguage = soup.find_all(itemprop="inLanguage")[0].text
        book.bookFormat = soup.find_all(itemprop="bookFormat")[0].text
        book.bookDescription = soup.find_all(itemprop="description")[0].text
        book.bookImgName = (soup.find_all(itemprop="image")[0]).get('src')

        for link in soup.find_all('a'):
            if link.get('href').startswith('http://filepi.com'):
                book.name = link.text
        return book

    def firefoxDownloadJob(self, book, baseUrl, number):
        '''The function of this method is to download link of given URL.'''
        directory_name = os.path.join(self.directory_name, str(number))
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
        for number in range(7016, 0, -1):
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
                logging.info("checking  Is this book already availble (downloaded)" + book.bookName)
#                 self.firefoxDownloadJob(book, baseUrl, number)
    
if __name__ == "__main__":
    print 'download started'
    it = DownloadItEbook()
    it.startDownload()
