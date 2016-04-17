'''
Created on 17-Apr-2016

@author: vijay
'''
import requests
import os
import urllib2
from src.metadata.book import Book, VolumeInfo
from bs4 import BeautifulSoup

class DownloadMetadataInfo():
    '''
    This class will download metadata from different web url.
    '''
    def __init__(self):
        self.searchText = None
        pass
    
    def doAmazonBookSerach(self, searchText=None):
        if searchText:
#             searchUrl = 'http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Ddigital-text&field-keywords=' + searchText
            searchUrl ="http://www.amazon.com/s/ref=nb_sb_ss_i_1_6?url=search-alias=stripbooks&field-keywords={}&sprefix={},aps,319".format(searchText, searchText)
#             print searchUrl
            payload = {'Host':"www.amazon.com", 
                       'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
                       'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       'Accept-Language':"en-US,en;q=0.5",
                       'Accept-Encoding':"gzip, deflate",
                       'Referer':"http://www.amazon.com/",
                       'Connection':"keep-alive"}
            with requests.Session() as c:
                r = c.get(searchUrl, params=payload)
                print(r.url)
#                 print r.status_code, r.headers['content-type'], r.encoding
                content = r.text
                with open("response.html", "w") as text_file:
#                     print content.encode('utf-8')
                    text_file.write(content.encode('utf-8'))
                    text_file.close()
                soup = BeautifulSoup(content)
                
                print soup.find_all(class_="s-result-item celwidget")[0]
                
        
        
        pass
    
    def readAnalyseFile(self):
        with open("response.txt", "w") as text_file:
            content = ''
            for line in text_file.readlines():
                print line
            soup = BeautifulSoup(content)
            print soup.find_all_next('img')
        
    def doGoogleSearch(self):
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + self.search.GetValue())
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
                
            path = os.path.join('/tmp', 'img')
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
                with open(path + os.sep + b.id + '.jpeg', 'wb') as f:
                    f.write(urllib2.urlopen(url).read())
            b.volumeInfo = volumeInfo
            b.bookPath = None
            listOfBooks.append(b)
        return listOfBooks   

if __name__ == '__main__':
    DownloadMetadataInfo().doAmazonBookSerach(searchText='python')
    pass
