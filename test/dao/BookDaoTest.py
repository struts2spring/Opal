'''
Created on 05-Dec-2015

@author: vijay
'''
import unittest
from src.dao.BookDao import CreateDatabase
# from src.selenium_download.itebook import Book


class CreateDatabaseTest(unittest.TestCase):
    
    def setUp(self):
        print 'setUp'
        self.createDatabase=CreateDatabase()
#         self.createDatabase.creatingDatabase()

    def tearDown(self):
        print 'tearDown'
#     def testFindBook(self):
#         print 'testFindBook'
#         createDatabase=CreateDatabase()
#         book=Book()
#         book.name='java'
# #         book.isbn='java'
# 
#         dbBookObj=Book()
#         dbBookObj.bookName=book.name
#         dbBookObj.isbn_13=book.isbn
#         books=createDatabase.findBook(dbBookObj)
#         for book in books:
#             print book
#         pass

    def testAddingData(self):
        print 'testAddingData'
        self.createDatabase.creatingDatabase()
        self.createDatabase.addingData()
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()