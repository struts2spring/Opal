import os
from src.dao.BookDao import CreateDatabase
from src.static.constant import Workspace

class FindingBook():
    def __init__(self):
        self.createDatabase = CreateDatabase()
        pass

    def searchingBook(self, searchText=None):
        books = list()
        if searchText != None and searchText != '':
            os.chdir(Workspace().path)
            books = self.createDatabase.findByBookName(searchText)
        else:
            books = self.findAllBooks()
        return books

    def findAllBooks(self):
        books = list()
        os.chdir(Workspace().path)
        books = self.createDatabase.findAllBook()
        return books

    def getMaxBookId(self):
        os.chdir(Workspace().path)
    
    def deleteBook(self, book):
        self.createDatabase.removeBook(book)
        print 'deletingBook'
        
