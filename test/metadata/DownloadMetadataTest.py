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
        
    def testDoAmazonBookSerach(self):
        print 'testDoAmazonBookSerach'
        lst=["python", "jumble", "easy", "difficult", "answer",  "xylophone"]
#         while True:
#         self.downloadMetadataInfo.doAmazonBookSerach(searchText= random.choice(lst))
        self.downloadMetadataInfo.doAmazonBookSerach(searchText= 'python')
#         self.downloadMetadataInfo.readAnalyseFile()
        pass
        
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()