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

class DownloadMetadataInfo():
    '''
    This class will download metadata from different web url.
    '''
    def __init__(self):
        self.searchText = None
        self.session = requests.Session()
        self.listOfBook = list()
        self.requestHeader = None
    
    def doAmazonBookSerach(self, searchText=None):
        if searchText:
#             searchUrl = 'http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Ddigital-text&field-keywords=' + searchText
            searchUrl = "http://www.amazon.com/s/ref=nb_sb_ss_i_1_6?url=search-alias=stripbooks&field-keywords={}&sprefix={},aps,319".format(searchText, searchText)
#             print searchUrl
            payload = {'Host':"www.amazon.com",
                       'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
                       'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       'Accept-Language':"en-US,en;q=0.5",
                       'Accept-Encoding':"gzip, deflate",
                       'Referer':"http://www.amazon.com/",
                       'Connection':"keep-alive"}
#             with requests.Session() as c:
            r = self.session.get(searchUrl, params=payload)
#             print(r.url)
            self.requestHeader = r.headers
#             print r.status_code, r.headers['content-type'], r.encoding
            content = r.text
            if r.status_code == 200:
                with open("response.html", "w") as text_file:
#                     print content.encode('utf-8')
                    text_file.write(content.encode('utf-8'))
                    text_file.close()
                soup = BeautifulSoup(content)
                
#                 el= soup.find_all(class_="s-result-item celwidget")[0]
#                 print el.find_all(class_="a-link-normal s-access-detail-page a-text-normal")
# class_="s-result-item celwidget",
                urlList = list()
                for link in soup.find_all(class_="a-link-normal s-access-detail-page a-text-normal"):
#                     print el
#                     x= el.find_all(class_="a-link-normal s-access-detail-page a-text-normal")
                    urlList.append(link.get('href'))
                for url in urlList:
                    b = Book()
                    b.id = url.split('/')[-1]
                    imgFileName = b.id + '.jpg'
#                     print imgFileName
                    self.getAmazonSingleBookInfo(imgFileName=imgFileName, bookUrl=url)
            else:
                self.doAmazonBookSerach(searchText)    
                
    def getAmazonSingleBookInfo(self, imgFileName, bookUrl=None):
        '''
        e.g. urls are given below.
        'http://www.amazon.com/Learning-Python-5th-Mark-Lutz/dp/1449355730',
        'http://www.amazon.com/Automate-Boring-Stuff-Python-Programming/dp/1593275994',
        '''
            
        payload = {'Host':"www.amazon.com",
           'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
           'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           'Accept-Language':"en-US,en;q=0.5",
           'Accept-Encoding':"gzip, deflate",
           'Referer':"http://www.amazon.com/",
           'Connection':"keep-alive"}
#         searchUrl = ''
        if self.requestHeader:
            payload = self.requestHeader
        print bookUrl, imgFileName 
#         with requests.Session() as c:
        r = self.session.get(bookUrl, params=payload)
#             print(r.url)
        print r.status_code
        if r.status_code == 200:
            content = r.text
            soup = BeautifulSoup(content)
            print r.url
            b = self.populateBookObj(htmlContent=soup, imgFileName=imgFileName)
#             print content
            el = soup.find(id="imgBlkFront", class_="a-dynamic-image")
            imgUrl = el['src']
            if not os.path.exists(os.path.join(b.localImagePath, b.imageFileName)):
                self.downloadUrl(imageUrl=imgUrl, imgFileName=imgFileName, destinationPath=Workspace().imagePath)
        else:
#             print r.text
            self.getAmazonSingleBookInfo(imgFileName, bookUrl)
            
            
    def populateBookObj(self, htmlContent=None, imgFileName=None):
        '''
        '''
        b = Book()
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
                if tag1.text == 'About the Author':
                    b.aboutAuthor = tag1.text
        if b.id == None:
            b.id = b.asin
        b.localImagePath = Workspace().imagePath
        b.imageFileName = imgFileName    
        b.bookPath = None
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
                self.downloadUrl(imageUrl=url, imgFileName=b.id + '.jpeg', destinationPath=Workspace().imagePath)
#                 with open(path + os.sep + b.id + '.jpeg', 'wb') as f:
#                     f.write(urllib2.urlopen(url).read())
            b.volumeInfo = volumeInfo
            b.bookPath = None
            listOfBooks.append(b)
        return listOfBooks   
    
    def downloadUrl(self, imageUrl=None, imgFileName=None, destinationPath=Workspace().imagePath):
        '''
        This function will download url.
        '''
        if not os.path.exists(destinationPath):
            os.mkdir(destinationPath)
        os.chdir(destinationPath)   
        try:
            with open(os.path.join(destinationPath, imgFileName), 'wb') as f:
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
#     downloadMetadataInfo.getAmazonSingleBookInfo(imgFileName='1449355730.jpg', bookUrl=bookUrl)
    downloadMetadataInfo.doAmazonBookSerach(searchText='java')
    print downloadMetadataInfo.listOfBook
    pass
