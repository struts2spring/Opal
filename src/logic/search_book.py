import os
from src.dao.BookDao import CreateDatabase
from src.static.constant import Workspace

class FindingBook():

    def searchingBook(self, searchText=None):
        books = list()
        if searchText != None and searchText != '':
            print '1.-searchingBook--->', os.getcwd()
#             os.chdir('/home/vijay/Documents/Aptana_Workspace/util/src/dao')
            print Workspace().path
            os.chdir(Workspace().path)
            print '2.--searchingBook-->', os.getcwd()
#             session = CreateDatabase().creatingDatabase()
#             CreateDatabase().addingData()
            books = CreateDatabase().findByBookName(searchText)
        else:
            books = self.findAllBooks()
        return books

    def findAllBooks(self):
        books = list()
        print '1.-findAllBooks--->', os.getcwd()
#         os.chdir('/home/vijay/Documents/Aptana_Workspace/util/src/dao')
        os.chdir(Workspace().path)
        print '2.--findAllBooks-->', os.getcwd()
#         session = CreateDatabase().creatingDatabase()
#         CreateDatabase().addingData()
        books = CreateDatabase().findAllBook()
        return books

    def getMaxBookId(self):
        os.chdir(Workspace().path)
        