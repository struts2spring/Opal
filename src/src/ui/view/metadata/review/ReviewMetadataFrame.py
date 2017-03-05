'''
Created on 08-May-2016

@author: vijay
'''
import wx
from src.ui.view.metadata.review.PhotoFrame import PropertyPhotoPanel
from src.metadata.book import Book
from src.logic.search_book import FindingBook
from src.ui.view.metadata.review.ReviewThumbCrtl import ThumbnailCtrl, \
    NativeImageHandler
from src.metadata.DownloadMetadata import DownloadMetadataInfo
from src.dao.online.OnlineBookDaoImpl import OnlineDatabase
from threading import Thread
import copy
from src.logic.ReadWriteJson import ReadWriteJsonInfo
from src.dao.Author import Author
import shutil
import os

class BookMetadata():
    
    def __init__(self):
        pass
    
class ReviewRow():
    pass




#----------------------------------------------------------------------------------------------------------------


class ReviewMetadataPanel(wx.Panel):
    '''
    This class review metadata.
    '''
    def __init__(self, parent, book):
        wx.Panel.__init__(self, parent)
        self.currentBook = book
        self.tempRowDict = None
        self.downloadMetadataInfo = DownloadMetadataInfo()
        self.onlineDatabase = OnlineDatabase()
        self.mainPanel = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        self.rowList = ["Title", "Authors", 'Series', 'Tags', 'Rating', 'Publisher', 'ISBN-13', 'ISBN-10', 'Language', 'Description', 'Cover']
        
#         self.mainPanel.SetBackgroundColour('#FFFFFF')
        self.mainBox = wx.StaticBox(self.mainPanel, -1, "main box")
        self.left_staticbox = wx.StaticBox(self.mainPanel, -1, "left box")
        self.right_staticbox = wx.StaticBox(self.mainPanel, -1, "right box")
        
        self.helptext = wx.StaticText(self.mainPanel, -1, "Please review downloaded metadata.")
        
        self.search = wx.SearchCtrl(self, size=wx.DefaultSize, style=wx.TE_PROCESS_ENTER)
        self.search.SetValue(self.currentBook.bookName)
        self.search.ShowCancelButton(True)
        self.searchCache = dict()
        self.info = wx.InfoBar(self)
        self.thumbnail = ThumbnailCtrl(self, imagehandler=NativeImageHandler)
        self.worker = None
        self.defaultSearch(self.currentBook.bookName)
        # Set up event handler for any worker thread results
#         EVT_RESULT(self, self.OnResult)

        # And indicate we don't have a worker thread yet
#         self.rowDic = dict()
        self.diffView(self.currentBook)
        
#         bitmap = wx.ArtProvider_GetBitmap(wx.ART_GO_BACK)
#         self.okButton = wx.Button(self.mainPanel, -1, 'ok') 
#         self.copyRightToLeftButton = wx.BitmapButton(self.mainPanel, -1, bitmap, (10, 10), style=wx.BORDER_DEFAULT)
        self.createButtonBar()
        self.SetProperties()
        self.doLayout()
        self.BindEvents()
        
    def OnResult(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            print('Computation aborted')
        else:
            
            # Process results here
            print('Computation Result: %s' % event.data)
            self.thumbnail.ShowDir(event.data)
        # In either event, the worker is done
        self.info.Dismiss()
#         self.worker = None
    def OnDoSearch(self, evt):
        print("OnDoSearch: " + self.search.GetValue())
        searchText = self.search.GetValue()
        self.defaultSearch(searchText)
#         listOfBooks = self.doGoogleSearch()
#         listOfBooks = list()
# #         self.doAmazonBookSerach()
#         searchListOfBook = self.doSearch(self.search.GetValue())
#         
#         print len(listOfBooks)
#         if len(searchListOfBook) > 0:
#             listOfBooks = searchListOfBook
#         self.thumbnail.ShowDir(listOfBooks)    
        
    def doSearch(self, searchText=None):
         
#         onlineDatabase = OnlineDatabase()
#         listOfBooks = downloadMetadataInfo.doGoogleSearch(searchText)
        if self.searchCache.has_key(searchText):
            listOfBooks = self.searchCache[searchText]
            print listOfBooks
        else:
            self.downloadMetadataInfo.doAmazonBookSerach(searchText, self.onlineDatabase)
            listOfBooks = self.downloadMetadataInfo.listOfBook
             
             
        self.searchCache[searchText] = listOfBooks
         
        self.onlineDatabase.addingData(listOfBooks)
        if self.downloadMetadataInfo.bookListInDatabase:
            for book in self.downloadMetadataInfo.bookListInDatabase:
                book.localImagePath = '/docs/new/image'
                book.imageFileName = book.bookImgName
                listOfBooks.append(book)
         
        return listOfBooks       
    
    def defaultSearch(self, searchText='python'):
        listOfBooks = list()
#         self.downloadMetadataInfo.doAmazonBookSerach(searchText, self.onlineDatabase)
        searchListOfBook = self.doSearch(searchText)
        
        print len(listOfBooks)
        if len(searchListOfBook) > 0:
            listOfBooks = []
        self.thumbnail.ShowDir(listOfBooks)

            
    def decodeProperty(self, book, key):
        decodedProperty = ''
        
        if book != None:
            authorName = list()
            try:
                for a in book.authors:
                    authorName.append(a.authorName)
            except:
                pass
            
            authorNameString = ','.join(authorName)
            publisher = ''
            try:
                if book.publisher :
                    publisher = book.publisher 
            except:
                pass
            
            self.keyValue = {
                           'Title':book.bookName,
                           'Authors':authorNameString,
                           'Series':str(book.tag or ''),
                           'Tags':str(book.tag or ''),
                           'Rating':str(book.rating or ''),
                           'Publisher':publisher,
                           'ISBN-13':str(book.isbn_13 or ''),
                           'ISBN-10':str(book.isbn_10 or ''),
                           'Language':str(book.inLanguage or ''),
                           'Description':str(book.bookDescription or ''),
                           'Cover':'',
                           }
            decodedProperty = self.keyValue[key]
        return decodedProperty

    def createButtonBar(self):
        self.acceptAll = wx.Button(self.mainPanel, -1, "Accept all")
        self.rejectAll = wx.Button(self.mainPanel, -1, "Reject all")
        self.previous = wx.Button(self.mainPanel, -1, "Previous")
        self.next = wx.Button(self.mainPanel, -1, "Next")
        self.done = wx.Button(self.mainPanel, -1, "Done")
        
    def diffView(self, lefBookInfo=None, rightBookInfo=None):
#         rowList = ["Title", "Authors", 'Series', 'Tags', 'Rating', 'Publisher', 'ISBN-13', 'ISBN-10', 'Language', 'Description', 'Cover']
#         rowList=[]
#         b = self.getABook()
#         book = Book()
#         book.bookPath = b.bookPath
#         book.bookImgName = b.bookImgName
        self.rowDict = dict()
        self.tempRowDict = dict()
        for idx, item in enumerate(self.rowList):
            print idx, item
            bitmap = wx.ArtProvider_GetBitmap(wx.ART_GO_BACK)
            self.reviewRow = ReviewRow()
            self.reviewRow.label = wx.StaticText(self.mainPanel, -1, item)
            self.reviewRow.copyRightToLeftButton = wx.BitmapButton(self.mainPanel, -1, bitmap, (10, 10), style=wx.BORDER_DEFAULT, name=str(idx))  
            self.reviewRow.copyRightToLeftButton.Bind(wx.EVT_BUTTON, self.onCopyRightToLeftButton)  
            if item == 'Cover':
                self.tempRowDict[idx] = lefBookInfo
                self.reviewRow.leftText = PropertyPhotoPanel(self.mainPanel, lefBookInfo)
                self.reviewRow.rightText = PropertyPhotoPanel(self.mainPanel, rightBookInfo)
            else:
                leftTextValue = self.decodeProperty(lefBookInfo, item)
                self.tempRowDict[idx] = leftTextValue
                
                self.reviewRow.leftText = wx.TextCtrl(self.mainPanel, -1, value=leftTextValue, size=(200, -1))
                self.reviewRow.rightText = wx.TextCtrl(self.mainPanel, -1, value=self.decodeProperty(rightBookInfo, item), size=(200, -1))
                 
            self.rowDict[idx] = self.reviewRow
#         return self.rowDict


    def onCopyRightToLeftButton(self, event):
        """
        This method is fired when its corresponding button is pressed
        """
        button = event.GetEventObject()
        labelText = self.rowDict[int(button.GetName())].label.GetLabel()
#         print "The button you pressed was labeled: " + button.GetLabel()
#         print "The button's name is " + button.GetName()
        if labelText == 'Cover':
            rightBookInfo = self.rowDict[int(button.GetName())].rightText.currentBook
            rightBookInfo.bookPath = rightBookInfo.localImagePath
            self.rowDict[int(button.GetName())].leftText.currentBook = rightBookInfo
            self.rowDict[int(button.GetName())].leftText.changeBitmapWorker()
        else:
            rightValue = self.rowDict[int(button.GetName())].rightText.GetValue()
            self.rowDict[int(button.GetName())].leftText.SetValue(rightValue)
#         button_id = event.GetId()
#         button_by_id = self.FindWindowById(button_id)
#         print "The button you pressed was labeled: " + button_by_id.GetLabel()
#         print "The button's name is " + button_by_id.GetName()
        
    def SetProperties(self):
        self.helptext.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Verdana"))
    def doLayout(self):
        
        #------------- Layout for button ---------------------
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        rowsizer.Add(self.acceptAll, 1)
        rowsizer.Add(self.rejectAll, 1)
        rowsizer.Add(self.previous, 1)
        rowsizer.Add(self.next, 1)
        rowsizer.Add(self.done, 1)
        #-------------------------------------------------------
        #------search and thumbnail-----------
        searchVbox = wx.BoxSizer(wx.VERTICAL)
        searchVbox.Add(self.search, 0, wx.EXPAND | wx.ALL, 0)
#         self.info = wx.InfoBar(self)
        searchVbox.Add(self.info, 0, wx.EXPAND | wx.ALL, 0)
        searchVbox.Add(self.thumbnail, 1, wx.EXPAND | wx.ALL, 0)
        #-------------------------------------------------------
        
        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        vBox = wx.BoxSizer(wx.VERTICAL)
        
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        
        leftBox = wx.BoxSizer(wx.VERTICAL)
        rightBox = wx.BoxSizer(wx.VERTICAL)
        hRow = wx.BoxSizer(wx.HORIZONTAL)
        centerBox = wx.BoxSizer(wx.VERTICAL) 
        centerBox.Add(wx.StaticText(self, -1, label=" "), 2, wx.EXPAND | wx.DOWN, 15) 
        
        for key, value in self.rowDict.iteritems():
            hLeftRow = wx.BoxSizer(wx.HORIZONTAL)
            hRightRow = wx.BoxSizer(wx.HORIZONTAL)
            hCenterRow = wx.BoxSizer(wx.VERTICAL) 
            
            
            hLeftRow.Add(value.label, 3, wx.ALL | wx.EXPAND, 1)
            hLeftRow.Add(value.leftText, 7, wx.ALL | wx.EXPAND, 1)
            if value.label.GetLabel() == 'Cover':
                hRightRow.Add(wx.StaticText(self, -1, label=" "), 1, wx.EXPAND | wx.UP, 500)
                hLeftRow.Add(wx.StaticText(self, -1, label=" "), 1, wx.EXPAND | wx.UP, 500)
                hCenterRow.Add(wx.StaticText(self, -1, label=" "), 1, wx.EXPAND | wx.UP, 10)
                hCenterRow.Add(value.copyRightToLeftButton, 9, wx.CENTER | wx.EXPAND)
                hCenterRow.Add(wx.StaticText(self, -1, label=" "), 1, wx.EXPAND | wx.UP, 50)
            else:
                hCenterRow.Add(value.copyRightToLeftButton, 1, wx.CENTER)
            centerBox.Add(hCenterRow , 8, wx.CENTER)
            
            hRightRow.Add(value.rightText, 2, wx.ALL | wx.EXPAND, 1)
            
            leftBox.Add(hLeftRow, 0, wx.ALL | wx.EXPAND, 0)
            rightBox.Add(hRightRow, 0, wx.ALL | wx.EXPAND, 0)

        
        leftStaticBoxSizer = wx.StaticBoxSizer(self.left_staticbox, wx.HORIZONTAL)
        
        leftStaticBoxSizer.Add(leftBox, 1, wx.ALL | wx.EXPAND, 10)  
        
        
        
#         rightBox.Add(self.bookNameRight)
        rightStaticBoxSizer = wx.StaticBoxSizer(self.right_staticbox, wx.HORIZONTAL)
        rightStaticBoxSizer.Add(rightBox, 1, wx.ALL | wx.EXPAND, 10)  
        
#         
        hBox.Add(leftStaticBoxSizer, 1, wx.EXPAND | wx.ALL, 0)
        hBox.Add(centerBox, 0, wx.EXPAND | wx.ALL, 0)
        hBox.Add(rightStaticBoxSizer, 1, wx.EXPAND | wx.ALL, 0)
        
        vBoxSizer = wx.StaticBoxSizer(self.mainBox, wx.VERTICAL) 
        
        vBox.Add(self.helptext, 0, wx.ALL | wx.ADJUST_MINSIZE, 2)
        vBoxSizer.Add(hBox, 1, wx.ALL | wx.EXPAND, 0) 
        vBoxSizer.Add(rowsizer, 0, wx.EXPAND)
        
        vBox.Add(vBoxSizer, 0, wx.ALL | wx.EXPAND, 0) 
        
        self.mainPanel.SetAutoLayout(True)
        self.mainPanel.SetSizer(vBox)
        vBox.Fit(self.mainPanel)
        vBox.SetSizeHints(self.mainPanel)
        mainsizer.Add(self.mainPanel, 1, wx.EXPAND | wx.ALL, 0)
        topsizer.Add(searchVbox, 1, wx.EXPAND | wx.ALL, 0)
        topsizer.Add(mainsizer, 2, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(topsizer)
        topsizer.Layout()  
    
#----------------------------------------------------------------------

    def BindEvents(self):
        self.Bind(wx.EVT_CLOSE, self.onClose)
#         self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.search)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search)
        self.acceptAll.Bind(wx.EVT_BUTTON, self.onAcceptAll)
        self.rejectAll.Bind(wx.EVT_BUTTON, self.onRejectAll)
        self.previous.Bind(wx.EVT_BUTTON, self.onPrevious)
        self.next.Bind(wx.EVT_BUTTON, self.onNext)
        self.done.Bind(wx.EVT_BUTTON, self.onDone)
        
        
        
#                 rowsizer.Add(self.acceptAll, 1)
#         rowsizer.Add(self.rejectAll, 1)
#         rowsizer.Add(self.previous, 1)
#         rowsizer.Add(self.next, 1)
#         rowsizer.Add(self.done, 1)
        
    def onClose(self, event):
        self.Destroy()
    def onAcceptAll(self, event):
        print 'onAcceptAll'
        for key, row in self.rowDict.items():
            if row.label.GetLabel() == 'Cover':
                self.rowDict[key].leftText.currentBook = row.rightText.currentBook
                self.rowDict[key].leftText.changeBitmapWorker()                    
            else:
                self.rowDict[key].leftText.SetValue(row.rightText.GetValue())
        
    def onRejectAll(self, event):
        print 'rejectAll'
        if self.tempRowDict != None:
#             self.rowDict = self.tempRowDict
            for key, val in self.tempRowDict.items():
                if self.rowDict[key].label.GetLabel() == 'Cover':
                    self.rowDict[key].leftText.currentBook = val
                    self.rowDict[key].leftText.changeBitmapWorker()                    
                else:
                    self.rowDict[key].leftText.SetValue(val)
                
            
    def onPrevious(self, event):
        print 'previous'
    def onNext(self, event):
        print 'next'
    def onDone(self, event):
        print 'done'
        authorList = list()
        
        for key, row in self.rowDict.items():
            if row.label.GetLabel() == 'Cover':
                imgFilePath = os.path.join(row.leftText.currentBook.bookPath, row.leftText.currentBook.bookImgName)
                destinationImgFilePath = os.path.join(self.currentBook.bookPath, self.currentBook.imageFileName)
                shutil.copy (imgFilePath, destinationImgFilePath)
            elif row.label.GetLabel() == 'Title':
                self.currentBook.bookName = row.leftText.GetValue()
            elif row.label.GetLabel() == 'Authors':
                author = Author()
                author.authorName = row.leftText.GetValue()
                authorList.append(author)
                self.currentBook.authors = authorList
            elif row.label.GetLabel() == 'Series':
                self.currentBook.series = row.leftText.GetValue()
            elif row.label.GetLabel() == 'Tags':
                self.currentBook.tag = row.leftText.GetValue()
            elif row.label.GetLabel() == 'Rating':
                self.currentBook.rating = row.leftText.GetValue()
            elif row.label.GetLabel() == 'Publisher':
                self.currentBook.publisher = row.leftText.GetValue()
            elif row.label.GetLabel() == 'ISBN-13':
                self.currentBook.isbn_13 = row.leftText.GetValue()
            elif row.label.GetLabel() == 'ISBN-10':
                self.currentBook.isbn_10 = row.leftText.GetValue()
            elif row.label.GetLabel() == 'Language':
                self.currentBook.inLanguage = row.leftText.GetValue()
                

                
                
        ReadWriteJsonInfo().writeJsonToDir(self.currentBook.bookPath, self.currentBook)
        
        
    def getABook(self):
        books = FindingBook().findAllBooks()
        book = None
        for b in books:
            book = b
            break
        return book
class ReviewFrame(wx.Frame):
    def __init__(self, parent, book):
        wx.Frame.__init__(self, parent, -1, title='Review metadata', size=(1700, 800))
        self.panel = ReviewMetadataPanel(self, book)          
        self.Show()
if __name__ == '__main__':
    books = FindingBook().findAllBooks()
    book = None
    for b in books:
        book = b
        break
    print book
    app = wx.App(0)
    frame = ReviewFrame(None, book)
    app.MainLoop()  
     


# VBox
#     vBoxSizer
#         hBox
#             StaticBox
#             StaticBox
        
