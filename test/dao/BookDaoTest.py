'''
Created on 05-Dec-2015

@author: vijay
'''
import unittest
from src.dao.BookDao import CreateDatabase
from src.selenium_download.itebook import Book


class CreateDatabaseTest(unittest.TestCase):


    def testFindBook(self):
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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()