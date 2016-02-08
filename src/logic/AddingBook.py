'''
Created on Jan 1, 2016

@author: vijay
'''
from PyPDF2.pdf import PdfFileReader
import copy
from datetime import datetime
import json
import os
import shutil

from src.dao.Author import Author
from src.dao.AuthorBookLink import AuthorBookLink
from src.dao.Book import Book
from src.dao.BookDao import CreateDatabase
from src.logic.BookImage import BookImage
from src.static.constant import Workspace
from src.util.remove import Util


class AddBook():
    '''
    This class have been written to add book to Opal workspace.
    '''


    def addingBookToWorkspace(self, sourcePath=None):

        '''
        This function will be creating a new dir. Get the max of id in Book table. Create the folder name with max of id plus one.
        @param sourcePath: This is the path of selected book.
        -1. Check if database present in workspace. There is possibility of a new workspace.
        0. Check if book already present in workspace.
        1. Create a folder with max_book_id+1 .
        2. Copy the book file in the directory.
        3. Create metadata i.e. (book.json)
        4. Make an entry in database.


        '''
        if sourcePath:
            createDatabase = CreateDatabase()
            maxBookId = createDatabase.getMaxBookID()
            if maxBookId == None:
                maxBookId = 0
            workspacePath = Workspace().path
            newDirPath = os.path.join(workspacePath, str(maxBookId + 1))

            # exatract file name from path.

            head, tail = os.path.split(sourcePath)
            self.book = Book()
            self.book.bookPath = newDirPath
            if tail.split(".")[-1:][0] == 'pdf':
                # reading pdf metadata.
                self.getPdfMetadata(sourcePath)
                if not self.book.bookName:
                    self.book.bookName = tail.split(".")[:1][0]

            print tail, 'file extension:', tail.split(".")[-1:][0]
            if not os.path.exists(newDirPath):
                os.makedirs(newDirPath)
                dest = os.path.join(newDirPath, tail)
                print sourcePath, '==>', dest
                shutil.copy (sourcePath, dest)
                name=tail.split(".")[:1][0]
                BookImage().getBookImage(newDirPath, name)
                self.book.inLanguage = 'English'
                self.book.hasCover = 'Y'

                book_copy1 = copy.deepcopy(self.book)
                book_copy2 = copy.deepcopy(self.book)
                self.writeBookJson(newDirPath, book_copy1)
                self.addingBookInfoInDatabase(self.book)


            else:
                '''
                say dir exist to the database by making an entry. And call itself.
            1. Check dir if it has book.
            2. remove dir if it does not contain any book (file).
            3. make an entry in database if it has book.
            4. go to the next directory
            '''
            os.chdir(newDirPath)
            print 'number of files:', len(os.listdir(newDirPath))
            if len(os.listdir(newDirPath)) > 0:
                for sName in os.listdir(newDirPath):
                    if os.path.isfile(os.path.join(newDirPath, sName)):
                        print sName
            else:
                os.chdir("..")
                os.removedirs(newDirPath)
#                     lst.append(sName.split('.')[-1:][0])
#                     files.append(os.path.join(directory_name, sName))
#             self.addingBookToWorkspace()

    def addingBookInfoInDatabase(self, book):
        '''
        This method will add new book info in database.
        '''
        createDatabase = CreateDatabase()
#         authorBookLink = AuthorBookLink()
#         author=Author()
#         book1=Book()
#         for b in book.__dict__:
#             if b not in ['_sa_instance_state','book_assoc']:
#                 print b
#
#         authorBookLink.author = book.authors
#         authorBookLink.book = book
        createDatabase.saveBook(book)

    def writeBookJson(self, newDirPath, book):
        '''
        This function will write book.json (metadata) of the newly added book in workspace.
        '''
        f = open(os.path.join(newDirPath , 'book.json'), 'w')
        row2dict = book.__dict__
        authors = []
        for a in row2dict['authors']:
            author = {}
            author = a.__dict__
            del author['_sa_instance_state']
            del author['book_assoc']
            authors.append(author)
        del row2dict['_sa_instance_state']
        del row2dict['authors']
        del row2dict['book_assoc']

        row2dict['authors'] = authors
        row2dict['publishedOn'] = str(datetime.now())
        row2dict['createdOn'] = str(datetime.now())
        f.write(json.dumps(row2dict, sort_keys=True, indent=4))

        f.close()

    def getPdfMetadata(self, path=None):
        '''
        This method will get the pdf metadata and return book object.
        '''

        print path

        if path:
            input = PdfFileReader(open(path, "rb"))
            print 'getPdfMetadata', input.getIsEncrypted()
        if path :
            pdf_toread = PdfFileReader(open(path, "rb"))
            if pdf_toread.isEncrypted:
                pdf_toread.decrypt('')
            pdf_info = pdf_toread.getDocumentInfo()
            print str(pdf_info)
            print 'Pages:', pdf_toread.getNumPages()
#             book = Book()
            if pdf_info.title != None:
                self.book.bookName = str(pdf_info.title)

            if pdf_info.creator:
                self.book.publisher = str(pdf_info.creator.encode('utf-8'))
            self.book.createdOn = datetime.now()
            try:
                print str(pdf_info['/CreationDate'])[2:10]
                date = datetime.strptime(str(pdf_info['/CreationDate'])[2:10] , '%Y%m%d')
                self.book.publishedOn = date
            except:
                print 'CreationDate not found'
            self.book.bookFormat = 'pdf'
            print path
            print Util().convert_bytes(os.path.getsize(path))
            self.book.fileSize = Util().convert_bytes(os.path.getsize(path))
            self.book.numberOfPages = pdf_toread.getNumPages()

            value = pdf_info.subject
            if type(pdf_info.subject) == str:
                # Ignore errors even if the string is not proper UTF-8 or has
                # broken marker bytes.
                # Python built-in function unicode() can do this.
                value = unicode(pdf_info.subject, "utf-8", errors="ignore")
            else:
                # Assume the value object has proper __unicode__() method
                value = unicode(pdf_info.subject)
                print 'else'

#             if 'ISBN'.lower() in str(pdf_info['/Subject']).lower():
#                 self.book.isbn_13 = str(pdf_info['/Subject'])[6:]

            author = Author()
            author.authorName = str(pdf_info.author)

            authorList = list()
            authorList.append(author)
            self.book.authors = authorList

            authorBookLink = AuthorBookLink()
            authorBookLink.author = author
            authorBookLink.book = self.book





if __name__ == '__main__':
#     sourcePath='C:\\Users\\vijay\\Downloads\\ST-52900095-16911.pdf'
#     sourcePath = 'C:\\Users\\vijay\\Downloads\\Head First Rails.pdf'
#     sys.set
    sourcePath = '/home/vijay/Downloads/1389095365492.pdf'
    AddBook().addingBookToWorkspace(sourcePath)
    pass
