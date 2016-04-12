'''
Created on 12-Apr-2016

@author: vijay
'''
import unittest


class Test(unittest.TestCase):
    
    def setUp(self):
        print 'setUp'
        self.createDatabase=CreateDatabase()
#         self.createDatabase.creatingDatabase()

    def tearDown(self):
        print 'tearDown'

    def testReadJsonFromDir(self, dirName='1'):
        pass
    
    def testWriteJsonToDir(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()