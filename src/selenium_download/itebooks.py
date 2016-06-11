
#http://itebooks.website/page-1000.html
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
from src.dao.BookDao import CreateDatabase
from src.static.constant import Workspace
import datetime
import traceback
from datetime import datetime
import requests
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary




class Book(json.JSONEncoder):
    def __init__(self, name=None, publisher=None, authors=None, isbn_13=None, datePublished=None, numberOfPages=None,
                 inLanguage=None, fileSize=None, bookFormat=None, bookDescription=None, bookImgName=None, bookSubTitle=None):
        '''
        Constructor
        '''
        self.bookName = name
        self.publisher = publisher
        
        self.authors = list()
        
        self.isbn_13 = isbn_13
        self.publishedOn = datePublished
        self.numberOfPages = numberOfPages
        self.inLanguage = inLanguage
        self.fileSize = fileSize
        self.bookFormat = bookFormat
        self.subTitle = bookSubTitle
        self.bookImgName=bookImgName
        self.itEbookUrlNumber = None

    def __str__(self):
        rep = self.name + self.publisher + self.author + self.isbn_13 + self.datePublished + self.numberOfPages + self.inLanguage + self.fileSize + self.bookFormat
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
        

class ItEbook(object):
    '''
    This class downloads first page of itebookinfo
    '''


    def __init__(self, baseUrl=None):
        '''
        Constructor
        '''
        self.baseUrl=baseUrl
        self.directory_name = Workspace().libraryPath
        self.createDatabase = CreateDatabase() 
        self.header_info={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'}
        pass

    def getUrl(self, baseUrl):
        '''this method will find and constuct all url of url given'''
        return self.baseUrl
    
    def findAllBookUrl(self, subUrl=None):
        '''
        This method retrive all the book url avaialbe in the page.
        http://itebooks.website/page-2.html
        '''
        url=self.baseUrl+'/'+subUrl
        print url
#         content = urllib2.urlopen(url).read()
        r = requests.get(url,headers=self.header_info,timeout=30)
        if r.status_code==200:
            soup = BeautifulSoup(r.content, "lxml")
        
            skipList=(u'\nCategories', u'\nContact', u'\nUpload', u'\nDonate',u'IT eBooks',  u'Prev', u'Next')
            listOfBookName=list()
            for link in soup.find_all('a'):
                if link.text.strip() !='' and link.text not in skipList:
                    listOfBookName.append(link.text)
                    
                    isBookAvailable=self.isBookNameAvailableInDatabase(link.text)
                    if not isBookAvailable :
                        print link.text, '\t',link.get('href'), isBookAvailable
                        book= self.findBookDetail(link.get('href'))
    #                     print book
                        try:
                            print 'uploading database'
                            self.firefoxDownloadJob(book,  link.get('href'))
                            self.updateDatabase()
                        except:
                            print link.get('href')
                            traceback.print_exc()
        
                        
    def updateDatabase(self):
        self.createDatabase.creatingDatabase()  
        self.createDatabase.addingData() 
           
    def isBookNameAvailableInDatabase(self,bookName=None):
        isBookPresent=False
        book= self.createDatabase.findByBookName(bookName)
        if book:
            isBookPresent=True
        return isBookPresent
      
    def findBookDetail(self, subUrl):
        ''' This method will download book cover.
         It will provide book object.'''
        book=None
        url=self.baseUrl+'/'+subUrl
        r = requests.get(url,headers=self.header_info,timeout=30)
        if r.status_code==200:
            soup = BeautifulSoup(r.content, "lxml")

            book = Book()
            book.authors.append(Author(soup.find_all(itemprop="author")[0].text))
            book.isbn_10 = soup.find_all(itemprop="isbn")[0].text
            book.isbn_13 = soup.find_all(itemprop="isbn")[1].text
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
            book.bookDescription = soup.find_all("div", {"class": "span12"})[3].text
            print soup.find_all(itemprop="image")
            book.bookImgName = (soup.find_all(itemprop="image")[0]).get('src')
            try:
                book.subTitle = soup.find_all("div", {"class": "span12"})[1].text
            except:
                traceback.print_exc()
                
#             book.fileSize = soup.find_all('table')[3].find_all('tr')[7].find_all('td')[1].find_all('b')[0].text
            book.fileSize = soup.find_all('table',{"class":"table table-bordered"})[1].find_all('tr')[5].find_all('td')[1].text
    #         book.fileSize=
    
    #         .top > div:nth-child(2) > h3:nth-child(2)
    
    
#             for link in soup.find_all('a'):
#                 if link.get('href').startswith('http://filepi.com'):
#                     book.name = link.text
#                     break
        return book

    def firefoxDownloadJob(self, book,  refUrl):
        '''The function of this method is to download link of given URL.'''
        # Creating directory
        directory_name = self.downloadDir()

        # Creating Actual URL
        url = self.baseUrl+refUrl


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

            imageUrl = self.baseUrl + book.bookImgName
            subUrl = book.bookImgName
            imageFileName = subUrl.split('/')[-1:][0]

            # Downloading book cover
            bookImagePath = os.path.join(directory_name, subUrl.split('/')[-1:][0])
#             urllib.urlretrieve(imageUrl,bookImagePath)
            from PIL import Image   
            from StringIO import StringIO
            r = requests.get(imageUrl,headers=self.header_info,timeout=30)
            print '--------------->',r.url
            with open(bookImagePath, 'wb') as imageFile:
                imageFile.write(r.content)
            
            book.bookImgName = imageFileName
            #writing json file
            self.writeJsonToDir(directory_name, book)
            binary = FirefoxBinary('/docs/python_projects/firefox/firefox')

            fp = webdriver.FirefoxProfile()

            fp.set_preference("webdriver.log.file", "/tmp/firefox_console");
            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference('browser.download.manager.showWhenStarting', True)
            fp.set_preference('browser.download.manager.focusWhenStarting', True)
            fp.set_preference("browser.download.dir", directory_name)
            fp.set_preference("browser.download.manager.scanWhenDone", True)
            fp.set_preference("browser.download.manager.useWindow", True)
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            fp.update_preferences()
            driver = webdriver.Firefox(firefox_profile=fp,firefox_binary=binary)
            # driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]/img")
            driver.get(url)
            efd_link = driver.find_element_by_id(id_='download')
#             efd_link.click()
            efd_link.send_keys(Keys.RETURN)
            flag = True
            while(flag):
                # # checking part file
                time.sleep(10)
                lst = []
                files=[]
                for sName in os.listdir(directory_name):
                    if os.path.isfile(os.path.join(directory_name, sName)):
                        lst.append(sName.split('.')[-1:][0])
                        files.append(os.path.join(directory_name, sName))
                print lst
                if 'part' not in lst:
                    flag = False
                    time.sleep(10)
                    driver.close()
                else:
                    #print files
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
#                 print len(list(size))
                if len(list(size)) > 1:
                    isDownloading=False
            checkFlagForSize=False
        logging.info('isDownloading:')
        return isDownloading


    def startDownload(self):
        baseUrl = 'http://itebooks.website'
        itebook = ItEbook(baseUrl)
            # TODO need to be updated
        logicTrue=True
        i=42
        while logicTrue:
            subUrl='page-'+str(i)+'.html'
            itebook.findAllBookUrl(subUrl)
            i=i+1
            print 'startDownload---------->',str(i)
#             if i==4:
#                 break

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
            os.chdir(directory_name)
        return directory_name



if __name__ == "__main__":
        
#         ItEbook().startDownload()
    ItEbook().startDownload()

