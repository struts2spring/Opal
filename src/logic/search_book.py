import os
from src.dao.BookDao import CreateDatabase
from src.static.constant import Workspace

class FindingBook():

    def searchingBook(self, searchText=None):
        books = list()
        if searchText != None and searchText != '':
            os.chdir(Workspace().path)
            books = CreateDatabase().findByBookName(searchText)
        else:
            books = self.findAllBooks()
        return books

    def findAllBooks(self):
        books = list()
        os.chdir(Workspace().path)
        books = CreateDatabase().findAllBook()
        return books

    def getMaxBookId(self):
        os.chdir(Workspace().path)
        