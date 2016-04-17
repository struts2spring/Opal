import unittest
from src.metadata.DownloadMetadata import DownloadMetadataInfo
import random



class DownloadMetadataInfoTest(unittest.TestCase):
    '''
    this class would be testing DownloadMetadataInfo.
    '''
    
    def setUp(self):
        self.downloadMetadataInfo=DownloadMetadataInfo()
        print 'setUp'

    def tearDown(self):
        print 'tearDown'
        
    @unittest.skip("demonstrating skipping")
    def testDoAmazonBookSerach(self):
        print 'testDoAmazonBookSerach'
        lst=["python", "jumble", "easy", "difficult", "answer",  "xylophone"]
#         while True:
#         self.downloadMetadataInfo.doAmazonBookSerach(searchText= random.choice(lst))
        self.downloadMetadataInfo.doAmazonBookSerach(searchText= 'python')
#         self.downloadMetadataInfo.readAnalyseFile()
        pass
        
    def testGetAmazonSingleBookInfo(self):
        urlList=[
#                 'http://www.amazon.com/s?ie=UTF8&page=1&rh=n%3A283155%2Ck%3Apython',
                'http://www.amazon.com/Learning-Python-5th-Mark-Lutz/dp/1449355730',
                'http://www.amazon.com/Automate-Boring-Stuff-Python-Programming/dp/1593275994',
                'http://www.amazon.com/Python-Crash-Course-Hands--Project-Based/dp/1593276036',
                'http://www.amazon.com/Fluent-Python-Luciano-Ramalho/dp/1491946008',
                'http://www.amazon.com/Python-Machine-Learning-Sebastian-Raschka/dp/1783555130',
                'http://www.amazon.com/Learn-Python-One-Well-Hands-/dp/1506094384',
                'http://www.amazon.com/Python-Pocket-Reference-OReilly/dp/1449357016',
                'http://www.amazon.com/Python-Programming-Introduction-Computer-Science/dp/1590282418',
                'http://www.amazon.com/Python-Data-Analysis-Wrangling-IPython/dp/1449319793',
                'http://www.amazon.com/Introducing-Python-Modern-Computing-Packages/dp/1449359361',
                'http://www.amazon.com/Python-Informatics-Dr-Charles-Severance/dp/1492339245',
                'http://www.amazon.com/Python-Cookbook-Third-David-Beazley/dp/1449340377'
                 ]
        ur=urlList[0]
        self.downloadMetadataInfo.getAmazonSingleBookInfo(ur)
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()