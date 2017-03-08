'''
Created on 17-Apr-2016

@author: vijay
'''
import requests
import os
import urllib2
from src.metadata.book import Book, VolumeInfo
from bs4 import BeautifulSoup
import uuid
import traceback
from src.static.constant import Workspace
from src.logic.online.OnlineBookLogic import OnlineBookInfoLogic
import random

class DownloadMetadataInfo():
    '''
    This class will download metadata from different web url.
    '''
    def __init__(self):
        self.searchText = None
        self.session = requests.Session()
        self.payload = {
                   'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0",
                   'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   'Accept-Language':"en-US,en;q=0.5",
                   'Accept-Encoding':"gzip, deflate",
                   'Connection':"keep-alive"}
        self.listOfBook = list()
        self.requestHeader = None
        self.isbnUrlDict = None
        self.bookListInDatabase = None
        print 'DownloadMetadataInfo construction completed'
    
    def generatePayload(self):
        choices = [
            'Mozilla/5.0 (Windows NT 5.2; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20110814 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.2; rv:9.0.1) Gecko/20100101 Firefox/9.0.1',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.78 Safari/532.5',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        ]

        choose = random.randint(0, len(choices)-1)
        
        payload = {'User-agent':choices[choose]}
        osType=['X11; Ubuntu; Linux x86_64', 'Windows NT']
        browserType=['Firefox', '']
        return payload
    def doAmazonBookSerach(self, searchText=None, onlineDatabase=None):
        
        if searchText:
            self.searchText = searchText
#             searchUrl = 'http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Ddigital-text&field-keywords=' + searchText
            searchUrl = "http://www.amazon.com/s/ref=nb_sb_ss_i_1_6?url=search-alias=stripbooks&field-keywords={}&sprefix={},aps,319".format(searchText, searchText)
#             print searchUrl
#             payload = {'Host':"www.amazon.com",
#                        'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
#                        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#                        'Accept-Language':"en-US,en;q=0.5",
#                        'Accept-Encoding':"gzip, deflate",
#                        'Connection':"keep-alive"}
            self.payload = self.generatePayload()
            
#             Host: www.amazon.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0
# Accept: image/png,image/*;q=0.8,*/*;q=0.5
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Referer: http://www.amazon.com/s/ref=nb_sb_ss_i_1_6?url=search-alias=stripbooks&field-keywords=Scrum%20Wegwijzer:%20Een%20kompas%20voor%20de%20bewuste%20reiziger%20(Dutch%20Edition)&sprefix=Scrum%20Wegwijzer:%20Een%20kompas%20voor%20de%20bewuste%20reiziger%20(Dutch%20Edition),aps,319&Connection=keep-alive&Accept-Language=en-US%2Cen%3Bq%3D0.5&Accept-Encoding=gzip%2C+deflate&Accept=text%2Fhtml%2Capplication%2Fxhtml%2Bxml%2Capplication%2Fxml%3Bq%3D0.9%2C%2A%2F%2A%3Bq%3D0.8&User-Agent=Mozilla%2F5.0+%28X11%3B+Ubuntu%3B+Linux+x86_64%3B+rv%3A44.0%29+Gecko%2F20100101+Firefox%2F44.0
# Cookie: p90x-info=A; x-wl-uid=1Ti6kmu7EbBlC8tFxFzWZ0/ODBjISYJ7qQ808eBft64aiz6RNAp/YuhCRV5Wx89seUw+Kz1LKTCE=; session-id-time=2082787201l; session-id=179-1840368-5373456; ubid-main=187-1126592-4490122; csm-hit=1HZNZXZGMZDE1Z3HQ4BZ+s-1VXKK7JQT8T5ZT78NW4E|1463819299758; session-token=AVoLNIMokageMbshCqpLxYUzbv0F9AX0NU0Y1TElFyYXj2OGe2gXtAmXejTaJE3c4p+uan73+BILNG0bdkFouJk9tK9erhvgyQmvpj1l7uAvwvtN9u6Aimqrv2L7EfsA7NVE0u599ZZQZca1Kwvn8pJam7W+PIw/3ap5vk+DfStDoBz+oC+pB+yMmckFXf2PN/s8riCJm1wEmgxhxw7+Ssk3hsRObUC875JljKUfDx4RKJyfsHeMVZxjQU8QO2Yr
# Connection: keep-alive
#             with requests.Session() as c:
            
            try:
                r = self.session.get(searchUrl, params=self.payload)
                self.requestHeader = r.headers
                content = r.text
                print(r.url)
    #             print r.status_code, r.headers['content-type'], r.encoding
                if r.status_code == 200:
                    soup = BeautifulSoup(content, "html.parser")
                    urlList = list()
                    isbnList = list()
                    self.isbnUrlDict = dict()
                    for link in soup.find_all(class_="a-link-normal s-access-detail-page a-text-normal"):
                        url = link.get('href')
                        isbn = url.split('/')[-1]
                        urlList.append(url)
                        isbnList.append(isbn)
                        self.isbnUrlDict[isbn] = url
                        
                    print urlList
                    print isbnList
                    onlineBookInfoLogic = OnlineBookInfoLogic(onlineDatabase)
                    
                    isbnListInDatabase = onlineBookInfoLogic.bookListInOnlineDatabase(isbnList)
                    self.bookListInDatabase = onlineBookInfoLogic.getBookInfoObjects(isbnListInDatabase)

                    
                    isbnSearchList = onlineBookInfoLogic.bookListNotInOnlineDatabase(isbnList)
                    print isbnSearchList
                    for isbn in isbnSearchList:
                        b = Book()
                        b.id = isbn
                        bookImgName = b.id + '.jpg'
                        print bookImgName
                        # Take decision if book present in database dont call URL
    #                     if not self.isBookAvailable():
                        url = self.isbnUrlDict[isbn]
                        self.getAmazonSingleBookInfo(bookImgName=bookImgName, bookUrl=url)
                else:
                    self.doAmazonBookSerach(searchText,onlineDatabase)    
            except:
                print traceback.print_exc()
                
                

         
    
    def getAmazonSingleBookInfo(self, bookImgName, bookUrl=None):
        '''
        e.g. urls are given below.
        'http://www.amazon.com/Learning-Python-5th-Mark-Lutz/dp/1449355730',
        'http://www.amazon.com/Automate-Boring-Stuff-Python-Programming/dp/1593275994',
        '''
            
#         payload = {'Host':"www.amazon.com",
#            'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
#            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#            'Accept-Language':"en-US,en;q=0.5",
#            'Accept-Encoding':"gzip, deflate",
#            'Referer':"http://www.amazon.com/",
#            'Connection':"keep-alive"}
#         searchUrl = ''
        if self.requestHeader:
            self.payload = self.generatePayload()
        print bookUrl, bookImgName 
#         with requests.Session() as c:.
        
        r = self.session.get(bookUrl, params=self.payload)
#             print(r.url)
        print r.status_code
        if r.status_code == 200:
            content = r.text
            soup = BeautifulSoup(content, "html.parser")
            print r.url
            b = self.populateBookObj(htmlContent=soup, bookImgName=bookImgName)
#             print content
            el = soup.find(id="imgBlkFront", class_="a-dynamic-image")
            imgUrl = el['src']
            if not os.path.exists(os.path.join(b.localImagePath, b.bookImgName)):
                self.downloadUrl(imageUrl=imgUrl, bookImgName=bookImgName, destinationPath=Workspace().imagePath)
        else:
#             print r.text
            self.getAmazonSingleBookInfo(bookImgName, bookUrl)
            
            
    def populateBookObj(self, htmlContent=None, bookImgName=None):
        '''
        '''
        b = Book()
        b.rating = '0'
        b.isbn_13 = None
        b.isbn_10 = None
        b.inLanguage = None
        b.bookDescription = None
        b.id = None
        el0 = htmlContent.find_all(id="productTitle")
        if el0 == None or len(el0) == 0:
            el0 = htmlContent.find_all(id="ebooksProductTitle")
            
        if el0:
            b.bookName = el0.pop().text
        el1 = htmlContent.find_all('div', class_="content")

        for tag in el1:
            if tag.ul:
                el01 = tag.ul.find_all('li')
                if el01:
                    for el02 in el01:
#                         print el02.id,el02.b, el02.text
                        if el02.b:
                            prop = el02.b.text
                            if prop == 'Series:':
                                b.series = el02.text.split(':')[1:][0]
                            if prop == 'ASIN:':
                                b.asin = el02.text.split(':')[1:][0]
                            if prop == 'Publication Date:':
                                b.publishedOn = el02.text.split(':')[1:][0]
                            if prop == 'Paperback:':
                                b.numberOfPages = el02.text.split(':')[1:][0]
                            if prop == 'Print Length:':
                                b.numberOfPages = el02.text.split(':')[1:][0]
                            if prop == 'Publisher:':
                                b.publisher = el02.text.split(':')[1:][0]
                            if prop == 'Language:':
                                b.inLanguage = el02.text.split(':')[1:][0]
                            if prop == 'ISBN-13:':
                                b.isbn_13 = el02.text.split(':')[1:][0]
                            if prop == 'ISBN-10:':
                                b.id = el02.text.split(':')[1:][0]
                                b.isbn_10 = el02.text.split(':')[1:][0]
                            if prop.strip() == 'Product Dimensions:':
                                b.dimension = el02.text.split(':')[1:][0].strip()
                            if prop.strip() == 'Average Customer Review:':
                                x = el02.find_all(class_="crAvgStars")[0]
                                b.rating = x.next()[2].text.split('out of')[0:1][0]
                            
                            
                                       
            el2 = tag.find_all('div', class_="productDescriptionWrapper")
            for tag1 in el2:
                if tag1.text == 'About the Author' or tag1.parent.h3.text == 'About the Author':
                    b.aboutAuthor = tag1.text
        if b.id == None:
            b.id = b.asin
        b.localImagePath = Workspace().imagePath
        b.bookImgName = bookImgName    
        b.imageFileName = bookImgName
        b.bookPath = None
        b.searchedText = self.searchText
        b.source = 'amazon.com'
        b.tag = ''
        
        self.listOfBook.append(b)    
        return b

        
    def doGoogleSearch(self, searchText=None):
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + searchText)
        json_data = r.json()
        items = json_data['items']
        listOfBooks = []
        for x in items:
        #     print x.keys()
            b = Book(x)
            volumeInfo = VolumeInfo(b['volumeInfo'])
            b.bookName = volumeInfo.title
#                volumeInfo.imageLinks['thumbnail']
            
            if volumeInfo.has_key('imageLinks'):
                url = str(volumeInfo.imageLinks['thumbnail'])
            else:
                url = "https://books.google.co.in/googlebooks/images/no_cover_thumb.gif"
                
            path = Workspace().imagePath
#             os.mkdir(tmp_path)
#             path = os.path.dirname(__file__) + os.sep + 'tmp'
            print path
            if not os.path.exists(path):
                os.mkdir(path)
            b.localImagePath = path 
#             + os.sep + b.id + '.jpeg'
            b.imageFileName = b.id + '.jpeg'
            if not os.path.exists(os.path.join(b.localImagePath, b.imageFileName)):
                os.chdir(path)
                print 'writing file'
                self.downloadUrl(imageUrl=url, bookImgName=b.id + '.jpeg', destinationPath=Workspace().imagePath)
#                 with open(path + os.sep + b.id + '.jpeg', 'wb') as f:
#                     f.write(urllib2.urlopen(url).read())
            b.volumeInfo = volumeInfo
            b.bookPath = None
            b.source = 'googleapis.com'
            listOfBooks.append(b)
        return listOfBooks   
    
    def downloadUrl(self, imageUrl=None, bookImgName=None, destinationPath=Workspace().imagePath):
        '''
        This function will download url.
        '''
        if not os.path.exists(destinationPath):
            os.mkdir(destinationPath)
        os.chdir(destinationPath)   
        try:
            with open(os.path.join(destinationPath, bookImgName), 'wb') as f:
                f.write(urllib2.urlopen(imageUrl).read())
        except :
            print 'unable to donwload url: ', imageUrl
            traceback.print_exc()
            

    def readAnalyseFile(self):
        with open("response.txt", "w") as text_file:
            content = ''    
            for line in text_file.readlines():
                print line
            soup = BeautifulSoup(content)
            print soup.find_all_next('img')
if __name__ == '__main__':
#     DownloadMetadataInfo().doAmazonBookSerach(searchText='python')
#     bookUrl = 'http://www.amazon.com/Learning-Python-5th-Mark-Lutz/dp/1449355730'
    downloadMetadataInfo = DownloadMetadataInfo()
#     downloadMetadataInfo.getAmazonSingleBookInfo(bookImgName='1449355730.jpg', bookUrl=bookUrl)
    downloadMetadataInfo.doAmazonBookSerach(searchText='Software in 30 Days How Agile Managers Beat the Odds, Delight Their Customers, And Leave Competitors In the Dust')
    print downloadMetadataInfo.listOfBook
    pass
