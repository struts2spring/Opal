import os
from src.dao.BookDao import CreateDatabase
from src.static.constant import Workspace

class FindingBook():
    def __init__(self):
        self.createDatabase = CreateDatabase()
        pass

    def searchingBook(self, searchText=None):
        '''
        This method return list of books matching with search text.
        @param searchText: may be a book name 
        '''
        books = list()
        if searchText != None and searchText != '':
            os.chdir(Workspace().path)
            books = self.createDatabase.findByBookName(searchText)
        else:
            books = self.findAllBooks()
        return books
    
    def findBookByNextMaxId(self, bookId=None):
        return self.createDatabase.findBookByNextMaxId(bookId)

    def findAllBooks(self):
        '''
        This method will give all the books list in book library.
        '''
        books = list()
        os.chdir(Workspace().path)
        books = self.createDatabase.findAllBook()
        return books

    def getMaxBookId(self):
        os.chdir(Workspace().path)
    
    def deleteBook(self, book):
        '''
        removing book from database and files.
        @param book: book object 
        '''
        self.createDatabase.removeBook(book)
        print 'deletingBook'
        
