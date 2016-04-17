import os
from src.dao.BookDao import CreateDatabase
from src.static.constant import Workspace
from src.logic.BookShellOperation import BookTerminal

class FindingBook():
    '''
    This class searches book detail in Opal database.this database would be created in workspace(Opal library).
    '''
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
    def findBookByPreviousMaxId(self, bookId=None):
        return self.createDatabase.findBookByPreviousMaxId(bookId)
    def findAllBooks(self):
        '''
        This method will give all the books list in book library.
        '''
        books = list()
        os.chdir(Workspace().path)
        books = self.createDatabase.findAllBook()
        return books

    def findBookByIsbn(self, isbn_13):
        bs = self.createDatabase.findBookByIsbn(isbn_13)
        return bs

    def getMaxBookId(self):
        os.chdir(Workspace().path)
    
    def deleteBook(self, book):
        '''
        removing book from database and files.
        @param book: book object 
        '''
        bookPath = book.bookPath
        isSuccessfulDatabaseDelete = self.createDatabase.removeBook(book)
        if isSuccessfulDatabaseDelete:
            BookTerminal().removeBook(bookPath=bookPath)
            
        print 'Book deleted'
        
