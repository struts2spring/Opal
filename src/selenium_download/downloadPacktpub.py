import urllib2
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import json
import os
from src.dao.BookDao import CreateDatabase
from src.static.constant import Workspace


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
    
    

class PacktpubCrawl:
    def __init__(self):
        self.baseUrl = "https://www.packtpub.com/"
        self.directory_name = Workspace().libraryPath
        self.createDatabase = CreateDatabase() 

    def findBookUrl(self):
        directory_name = '.'
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
        driver.get(self.baseUrl)
        efd_link = driver.find_element_by_css_selector(".login-popup > div:nth-child(1)")
        efd_link.click()
        try:
            emailEl = driver.find_element_by_css_selector('#packt-user-login-form > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)')
#             emailEl = driver.find_element_by_name("email")
            '''
            Login with user credential
            '''
            emailEl.send_keys('view7677@gmail.com')
            passwordEl = driver.find_element_by_css_selector("#packt-user-login-form > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)")
            passwordEl.send_keys('default')
            loginEl = driver.find_element_by_css_selector("#packt-user-login-form > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)")
            loginEl.click()
            
            if True:
                '''
                clicking on My Account
                '''
                myAccountEl = driver.find_element_by_css_selector('#account-bar-logged-in > a:nth-child(1) > div:nth-child(1) > strong:nth-child(1)')
                myAccountEl.click()
                
                '''
                clicking My ebooks
                '''
                myEbook = driver.get(self.baseUrl + 'account/my-ebooks')
                productListEls = driver.find_elements_by_css_selector('div.product-line')
                print len(productListEls)
                bookList = list()
                for productEl in productListEls:
                    print productEl
                    
                    try:
                        bookName = productEl.find_element_by_css_selector('.title').text
                        book = self.createBookDetail(bookName)
                        productEl.click()
                        readMeEl = productEl.find_element_by_css_selector('.fake-button-text')
                        print 'new page',
                        isbnEl = productEl.find_elements_by_css_selector('div > div:nth-child(2) > div:nth-child(1)> a:nth-child(1) > div:nth-child(1)')
                        book.isbn_13 = isbnEl[0].get_attribute('isbn')
#                     readMeEl.click()
                        print 'div.product-line:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1)',
#                     readMeEl.find_element_by_css_selector('h2.ng-binding')
#                     
#                     readingEl = driver.get('https://www.packtpub.com/mapt/book/All%20Books/' + book.isbn_13)
#                     bookName1=driver.find_elements_by_css_selector('h2.ng-binding')[0].text
                    
                        bookList.append(book)
                    except Exception as e:
                        print e
#                 product_account_list_el=driver.find_elements_by_css_selector('#product-account-list')
            
            driver.get('https://www.packtpub.com/packt/offers/free-learning')
            try:
                '''
                clicking on Claim your free ebook
                '''
                bookNameEl_1 = driver.find_element_by_css_selector('.dotd-title > h2:nth-child(1)')
                isBookAlreadyAvailable = False
                bookName_1 = bookNameEl_1.text
                for book in bookList:
                    if bookName_1 in book.bookName:
                        isBookAlreadyAvailable = True
                        break
                        
                if not isBookAlreadyAvailable:
                    claimFreeEbookEl = driver.find_element_by_css_selector('.book-claim-token-inner > input:nth-child(3)')
                    claimFreeEbookEl.click()
            except Exception as e:
                print e
                
#             myEbook.click()
            
        except Exception as e:
            print e
        finally:
            print 'completed'
        print 'hi'

    def createBookDetail(self, bookName=None):
        book = Book()   
        book.bookName = bookName
        book.bookFormat = 'pdf'
        book.tag = 'Technology'
        book.inLanguage = 'English'
        book.subTitle = None
        book.publisher = "Packt Publishing Limited"
        book.bookImgName = bookName + '.jpg'
        book.hasCover = 'Yes'
        book.hasCode = None
        
        return book
    
    def getMaxBookID(self):
        '''
        This function will get max book id.
        @param number:it takes database maxId+1 to create new directory . 
        '''
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
    PacktpubCrawl().findBookUrl()
    print 'pass'
