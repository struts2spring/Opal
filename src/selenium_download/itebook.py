from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import logging
import logging
import os
import sys
import time
import unittest
import urllib
import urllib2

import os

global directory_name
directory_name= '/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books'
# listOfDir = os.listdir(directory_name)
# listOfDir.sort()

listOfDir = [ name for name in os.listdir(directory_name) if os.path.isdir(os.path.join(directory_name, name)) ]
if listOfDir:
    listOfDir.sort(key=int)

listOfDirNotAvailable=list()

maxNum=3404
x=1
for i in range(2,int(maxNum)-2):
    print int(listOfDir[i-1]),i
    if listOfDir[i-x] != str(i):
        x=x+1
        listOfDirNotAvailable.append(i)



# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='myapp.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# create logger
logger = logging.getLogger('it-ebook')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('itebook.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')


class Book(json.JSONEncoder):
    def __init__(self, name=None, publisher=None, author=None, isbn=None, datePublished=None, numberOfPages=None, inLanguage=None, fileSize=None, bookFormat=None, bookDescription=None, image=None):
        '''
        Constructor
        '''
        self.name = name
        self.publisher = publisher
        self.author = author
        self.isbn = isbn
        self.datePublished = datePublished
        self.numberOfPages = numberOfPages
        self.inLanguage = inLanguage
        self.fileSize = fileSize
        self.bookFormat = bookFormat

    def __str__(self):
        rep = self.name + self.publisher + self.author + self.isbn + self.datePublished + self.numberOfPages + self.inLanguage + self.fileSize + self.bookFormat
        return rep


class ItEbook(object):


    def __init__(self):
        '''
        Constructor
        '''
        pass

    def getUrl(self, baseUrl, number):
        '''this method will find and constuct all url of url given'''
        return baseUrl + '/book/' + str(number)

    def findBookDetail(self, baseUrl, number):
        ''' This method will download book cover.
         It will provide book object.'''
        url = ItEbook().getUrl(baseUrl, number)
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
        book = Book()
        book.author = soup.find_all(itemprop="author")[0].text
        book.isbn = soup.find_all(itemprop="isbn")[0].text
        book.bookName = soup.find_all(itemprop="name")[0].text
        book.publisher = soup.find_all(itemprop="publisher")[0].text
        book.datePublished = soup.find_all(itemprop="datePublished")[0].text
        book.numberOfPages = soup.find_all(itemprop="numberOfPages")[0].text
        book.inLanguage = soup.find_all(itemprop="inLanguage")[0].text
        book.bookFormat = soup.find_all(itemprop="bookFormat")[0].text
        book.bookDescription = soup.find_all(itemprop="description")[0].text
        book.image = (soup.find_all(itemprop="image")[0]).get('src')

        for link in soup.find_all('a'):
            if link.get('href').startswith('http://filepi.com'):
                book.name = link.text
        return book

    def firefoxDownloadJob(self, book, baseUrl, number):
        '''The function of this method is to download link of given URL.'''
        global directory_name
        # Creating directory
        directory_name = directory_name  + str(number)

        # Creating Actual URL
        url = ItEbook().getUrl(baseUrl, number)
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        lsFiles = []
        logger.info(os.listdir(directory_name))

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

            imageUrl = url + book.image
            logger.info(imageUrl)
            subUrl = book.image

            # Downloading book cover
            urllib.urlretrieve(baseUrl + book.image, directory_name + str(number) + '/' + subUrl.split('/')[-1:][0])

            f = open(os.getcwd() + '/books/' + str(number) + '/book.json', 'w')
            f.write(json.dumps(book.__dict__, sort_keys=False, indent=4))
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
                files=[]
                for sName in os.listdir(directory_name):
                    if os.path.isfile(os.path.join(directory_name, sName)):
                        logger.info( sName.split('.')[-1:][0])
                        lst.append(sName.split('.')[-1:][0])
                        files.append(os.path.join(directory_name, sName))
                print lst
                if 'part' not in lst:
                    logger.info("flag :" + str(flag) )
                    flag = False
                    time.sleep(10)
                    driver.close()
                else:
                    #print files
#                     if not self.isBookDownloading(files):
#                         driver.close()
                    pass


    def isBookDownloading(self, files):
        ''' This method will inform that book is getting downloading or not.'''
        #time.sleep(2)
        dic_files={}
        time_dic_files={}
        i=1
        checkFlagForSize=True
        isDownloading=True
        for fl in files:
            dic_files[fl]=str(os.stat(fl).st_size)
        while(checkFlagForSize):

            time_dic_files[i]=dic_files
            i=i+1
            if i>4:
                size=set()
                for k in time_dic_files[i-1]:
                    if 'part' in k:
                        size.add(time_dic_files[i-1][k])
                for k in time_dic_files[i-2]:
                    if 'part' in k:
                          size.add(time_dic_files[i-2][k])
                for k in time_dic_files[i-3]:
                    if 'part' in k:
                        size.add(time_dic_files[i-3][k])
                print len(list(size))
                if len(list(size)) > 1:
                    isDownloading=False
            checkFlagForSize=False
        logging.info('isDownloading:')
        return isDownloading


    def startDownload(self):
        baseUrl = 'http://it-ebooks.info'
        itebook = ItEbook()
        for number in range(5214, 5982):
            url = ItEbook().getUrl(baseUrl, number)
            logger.info("Downloading " + url )
            a = urllib.urlopen(url)
            strig = a.geturl()
            if  '404' != strig[-4:-1]:
                book = itebook.findBookDetail(baseUrl, number)
                # Is this book already availble (downloaded)

                logger.info("checking  Is this book already availble (downloaded)" +book.bookName)
                itebook.firefoxDownloadJob(book, baseUrl, number)



if __name__ == "__main__":
        logger.info('start')
        ItEbook().startDownload()


