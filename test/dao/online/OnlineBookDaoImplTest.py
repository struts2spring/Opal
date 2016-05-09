
import unittest
from src.dao.online.OnlineBookDaoImpl import OnlineDatabase

class OnlineDatabaseTest(unittest.TestCase):
    def setUp(self):
        print 'setUp'
        self.onlineDatabase=OnlineDatabase()
#         self.createDatabase.creatingDatabase()

    def tearDown(self):
        print 'tearDown'
        
    def testfindBookInfo(self):
        print 'testfindBookInfo'
        self.onlineDatabase
        isbnList=['0071809252', '0071808558', '0596009208', 'B01BYGN93S', '0321356683', '0134177304', '1118407814', '1530011396', '0672337029', '1449370829', '1119272092']
        result = self.onlineDatabase.findBookInfo(isbnList)
        print result
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
