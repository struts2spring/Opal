
# http://itebooks.website/page-1000.html
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
import rarfile
from selenium.webdriver.common.action_chains import ActionChains




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
        self.itEbookUrlNumber = None
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
        

class ItEbook(object):
    '''
    This class downloads first page of itebookinfo
    '''


    def __init__(self, baseUrl=None):
        '''
        Constructor
        '''
        self.baseUrl = baseUrl
        self.directory_name = Workspace().libraryPath
        self.createDatabase = CreateDatabase() 
        self.header_info = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'}
        
        # book image url
        self.imageUrl = None
        self.bookUrl = None
        pass

    def getUrl(self, baseUrl):
        '''this method will find and constuct all url of url given'''
        return self.baseUrl
    
    def findAllBookUrl(self, subUrl=None):
        '''
        This method retrive all the book url avaialbe in the page.
        http://itebooks.website/page-2.html
        '''
        url = self.baseUrl + '/' + subUrl
#         print url
#         content = urllib2.urlopen(url).read()
        r = requests.get(url, headers=self.header_info, timeout=30)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
        
            skipList = [
                       'HOME',
                        'Category',
                        'Animals',
                        'Architecture',
                        'Art',
                        'Astronomy',
                        'Biography',
                        'Biology',
                        'Business',
                        'Chemistry',
                        'Cinema',
                        'Cookbooks',
                        'Cryptography',
                        'Culture',
                        'Design',
                        'Drawing',
                        'Economics',
                        'Encyclopedia and Dictionary',
                        'Engineering and Technology',
                        'Family and Friendship',
                        'Fitness',
                        'Gambling',
                        'Games',
                        'Hardware',
                        'Healthcare',
                        'History',
                        'Hobbies',
                        'Information Technologies',
                        'IT ebooks',
                        'Languages',
                        'Martial Arts',
                        'Mathematics',
                        'Medicine',
                        'Military',
                        'Music',
                        'Novels',
                        'Other',
                        'Personality',
                        'Philosophy',
                        'Photo',
                        'Physics',
                        'Poetry',
                        'Politics and Sociology',
                        'Programming',
                        'Psychology',
                        'Relationships',
                        'Religion',
                        'Science',
                        'Security',
                        'Sexuality',
                        'Software',
                        'Sport',
                        'Travel',
                        'Web Development'
                       ]
#             with open(os.path.dirname(__file__) + os.sep + 'skipList.txt', 'r') as f:
#                 for line in f:
#                     skipList.append(line.rstrip('\n'))
#                 f.close
            listOfBookName = list()
            for link in soup.find_all('a', 'title'):
                if link.text.strip() != '' and link.text not in skipList:
                    
                    listOfBookName.append(link.text)

                    isBookAvailable = self.isBookNameAvailableInDatabase(link.text)
#                     self.isIsbnAvailableInDatabase()
#                     print isBookAvailable, link.text
                    if not isBookAvailable :
#                         print link.text, '\t', link.get('href'), isBookAvailable
                        book, bookUrl = self.findBookDetail(link.get('href'))
                        isBookAvailable= self.isIsbnAvailableInDatabase(book.isbn_13)
    #                     print book
                        if not isBookAvailable :
                            try:
                                print 'uploading database'
                                directory_name = self.downloadEbook(book, link.get('href'), bookUrl)
                                self.updateDatabase(directory_name)
                            except:
                                print link.get('href')
                                traceback.print_exc()
        
                        
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
      
    def findBookDetail(self, subUrl):
        ''' This method will download book cover.
        It will provide book object.
        http://www.ebook777.com/shut-youre-welcome/
         '''
        book = None
#         url=self.baseUrl+'/'+subUrl
        url = subUrl
        r = requests.get(url, headers=self.header_info, timeout=30)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")

            book = Book()
            book.bookDescription = soup.find(id="main-content-inner").p.text
            book.bookName = soup.find(id="main-content-inner").find(class_='article-details').find(class_='title').text
            book.subTitle = soup.find(id="main-content-inner").find(class_='article-details').find(class_='subtitle').text
            bookUrl = soup.find(id="main-content-inner").find(class_='download-links').find('a')['href']
            table_body = soup.find('table')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 3:
                    book.bookImgName = cols[0].img.attrs['alt']
                    self.imageUrl = cols[0].img.attrs['src']
                    if cols[1].text == 'Author':
#                         print cols[2].text
                        author = Author()
                        author.authorName = cols[2].text
                        book.authors.append(author)
#                         book.authors.append()
                    
                if len(cols) == 2:
                    if cols[0].text == 'File size':
                        book.fileSize = cols[1].text
                    if cols[0].text == 'Year':
                        try:
                            date = datetime.strptime(cols[1].text , '%Y')
                        except:
                            date = datetime.now()
                        book.publishedOn = date
                    if cols[0].text == 'Pages':
                        book.numberOfPages = cols[1].text
                    if cols[0].text == 'Language':
                        book.inLanguage = cols[1].text
                    if cols[0].text == 'File format':
                        book.bookFormat = cols[1].text
                    if cols[0].text == 'Category':
                        book.tag = cols[1].text
                    if cols[0].text == 'File format':
                        book.bookFormat = cols[1].text
                    if cols[0].text == 'Isbn':
                        book.isbn_13 = cols[1].text

#                 print cols

        return book, bookUrl

    def downloadEbook(self, book, refUrl, bookUrl):
        directory_name = self.downloadDir()
        url = refUrl
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
        return directory_name
        
    def firefoxDownloadJob(self, book, refUrl):
        '''The function of this method is to download link of given URL.'''
        # Creating directory
        directory_name = self.downloadDir()

        # Creating Actual URL
#         url = self.baseUrl+refUrl
        url = refUrl


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

            # Downloading book cover
            bookImagePath = os.path.join(directory_name, book.bookImgName)
            self.downloadBookImage(bookImagePath, self.imageUrl)

            # writing json file
            self.writeJsonToDir(directory_name, book)
            binary = FirefoxBinary('/docs/python_projects/firefox/firefox')

            fp = webdriver.FirefoxProfile()

            fp.set_preference("webdriver.log.file", "/tmp/firefox_console");
            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference('browser.download.manager.showWhenStarting', False)
            fp.set_preference('browser.download.manager.focusWhenStarting', False)
            fp.set_preference("browser.download.dir", directory_name)
            fp.set_preference("browser.download.manager.scanWhenDone", False)
            fp.set_preference("browser.download.manager.useWindow", False)
#             fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/xml,application/pdf,text/plain,text/xml,image/jpeg,text/csv,application/zip,application/x-rar-compressed");
            fp.set_preference("browser.helperApps.alwaysAsk.force", False);
            fp.set_preference("browser.popups.showPopupBlocker", False);
            fp.update_preferences()
            driver = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary)
            # driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]/img")
            driver.get(url)
            efd_link = driver.find_element_by_css_selector(".download-links > a:nth-child(1)")
            efd_link.click()

#             efd_link.send_keys(Keys.RETURN)
            flag = True
            while(flag):
                # # checking part file
                time.sleep(10)
                lst = []
                files = []
                for sName in os.listdir(directory_name):
                    if os.path.isfile(os.path.join(directory_name, sName)):
                        lst.append(sName.split('.')[-1:][0])
                        files.append(os.path.join(directory_name, sName))
#                 print lst
                if 'part' not in lst:
                    flag = False
                    time.sleep(10)
                    driver.close()
                else:
                    # print files
#                     if not self.isBookDownloading(files):
#                         driver.close()
                    pass
        self.extractRar(directory_name)     
    
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
            if not row2dict['isbn_13'] ==None:
                if str(row2dict['isbn_13']).strip()=='':
                    row2dict['isbn_13']=None
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
#         baseUrl = 'http://itebooks.website'
#         baseUrl = 'http://it-ebooks.directory'
        baseUrl = 'http://www.ebook777.com'
        itebook = ItEbook(baseUrl)
            # TODO need to be updated
        logicTrue = True
        i =1100
        while logicTrue:
            subUrl = 'page/' + str(i) + '/'
            itebook.findAllBookUrl(subUrl)
            i = i + 1
            print 'startDownload---------->', str(i)
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

    def extractRar(self, directory_name):
        '''
        extracting rar file
        '''
        os.chdir(directory_name)
#         directory_name = '/docs/new/library/8006'
        listOfFiles = [ name for name in os.listdir(directory_name) if not os.path.isdir(os.path.join(directory_name, name)) ]
        for fileName in listOfFiles:
            if fileName.endswith(".rar"):
#                 print fileName
                directory_name
                rar = rarfile.RarFile(os.path.join(directory_name, fileName))
#                 print rar.namelist()
                infoList = rar.infolist()
                nameList = rar.namelist()
                for name in nameList:
                    if not ((name.endswith('.html')) or (name.endswith('.htm'))or (name.endswith('.txt'))) :
                        rar.extract(name, directory_name)
        pass

if __name__ == "__main__":
        
#         ItEbook().startDownload()
#     ItEbook().startDownload()
#     http://www.ebook777.com/shut-youre-welcome/
    itebook = ItEbook()
    itebook.startDownload()
#     itebook.baseUrl='http://www.ebook777.com'
#     subUrl='shut-youre-welcome'
#     refUrl="/"+subUrl
#     book=itebook.findBookDetail(subUrl)
#     itebook.firefoxDownloadJob(book, refUrl)
#     itebook.extractRar()
    

