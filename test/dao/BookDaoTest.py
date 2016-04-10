'''
Created on 05-Dec-2015

@author: vijay
'''
import unittest
from src.dao.BookDao import CreateDatabase
# from src.selenium_download.itebook import Book
from src.dao.Book import  Book


class CreateDatabaseTest(unittest.TestCase):
    
    def setUp(self):
        print 'setUp'
        self.createDatabase=CreateDatabase()
#         self.createDatabase.creatingDatabase()

    def tearDown(self):
        print 'tearDown'
        
    @unittest.skip("demonstrating skipping")
    def testFindBook(self):
        print 'testFindBook'
        createDatabase=CreateDatabase()
        book=Book()
        book.name='java'
#         book.isbn='java'
 
        dbBookObj=Book()
        dbBookObj.bookName=book.name
        dbBookObj.isbn_13=book.isbn
        books=createDatabase.findBook(dbBookObj)
        for book in books:
            print book
        pass
    @unittest.skip("demonstrating skipping")
    def testAddingData(self):
        print 'testAddingData'
        self.createDatabase.creatingDatabase()
        self.createDatabase.addingData()
        
    def testRemoveBook(self):
        print 'testRemoveBook'
        book=Book()
        book.id=1
        isSuccessfulDelete=self.createDatabase.removeBook(book)
        print isSuccessfulDelete
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()