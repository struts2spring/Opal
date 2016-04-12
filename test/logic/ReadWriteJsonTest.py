'''
Created on 12-Apr-2016

@author: vijay
'''
import unittest
from src.logic.ReadWriteJson import ReadWriteJsonInfo


class Test(unittest.TestCase):
    
    def setUp(self):
        print 'setUp'
        self.readWriteJson = ReadWriteJsonInfo()
#         self.createDatabase.creatingDatabase()

    def tearDown(self):
        print 'tearDown'

    def testReadJsonFromDir(self, dirName='1'):
        b=self.readWriteJson.readJsonFromDir(dirName)
        print b
        pass
    
    def testWriteJsonToDir(self):
        self.readWriteJson.writeJsonToDir(bookPath=None, book=None)
        pass

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
