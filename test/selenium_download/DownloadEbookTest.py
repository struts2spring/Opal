'''
Created on 09-Apr-2016

@author: vijay
'''
import unittest
from src.selenium_download.DownloadEbook import DownloadItEbook


class Test(unittest.TestCase):


    def setUp(self):
        self.downloadItEbook = DownloadItEbook()
        


    def tearDown(self):
        pass
    
    @unittest.skip("demonstrating skipping")
    def testDownloadDir(self):
        print 'testDownloadDir'
        self.downloadItEbook.downloadDir()
        
    @unittest.skip("demonstrating skipping")
    def testStartDownload(self):
        self.downloadItEbook.startDownload()
        pass
    
    @unittest.skip("demonstrating skipping")
    def testFindBookDetail(self): 
        baseUrl = 'http://it-ebooks.info'
        number=7102
#         genUrl=self.downloadItEbook.getUrl(baseUrl, number)
        self.downloadItEbook.findBookDetail(baseUrl, number)
        print 'testFindBookDetail'

    def testWriteJsonToDir(self):
        baseUrl = 'http://it-ebooks.info'
        number=7102
#         genUrl=self.downloadItEbook.getUrl(baseUrl, number)
        book=self.downloadItEbook.findBookDetail(baseUrl, number)
        self.downloadItEbook.writeJsonToDir(self.downloadItEbook.downloadDir(), book)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testStartDownload']
    unittest.main()