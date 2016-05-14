'''
Created on 08-May-2016

@author: vijay
'''
import wx
from src.ui.view.metadata.review.PhotoFrame import PropertyPhotoPanel
from src.metadata.book import Book
from src.logic.search_book import FindingBook


class ReviewRow():
    pass
class ReviewMetadataPanel(wx.Panel):
    '''
    This class review metadata.
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.mainPanel = wx.Panel(self, -1,style=wx.SIMPLE_BORDER)
#         self.mainPanel.SetBackgroundColour('#FFFFFF')
        self.mainBox = wx.StaticBox(self.mainPanel, -1, "main box")
        self.left_staticbox = wx.StaticBox(self.mainPanel, -1, "left box")
        self.right_staticbox = wx.StaticBox(self.mainPanel, -1, "right box")
        
        self.helptext = wx.StaticText(self.mainPanel, -1, "Please review downloaded metadata.")
#         self.rowDic = dict()
        self.diffView()
        
#         bitmap = wx.ArtProvider_GetBitmap(wx.ART_GO_BACK)
#         self.okButton = wx.Button(self.mainPanel, -1, 'ok') 
#         self.copyRightToLeftButton = wx.BitmapButton(self.mainPanel, -1, bitmap, (10, 10), style=wx.BORDER_DEFAULT)
        self.SetProperties()
        self.doLayout()
        self.BindEvents()
    
    def diffView(self):
        rowList = ["Title", "Authors", 'Series', 'Tags', 'Rating', 'Publisher', 'ISBN-13', 'ISBN-10', 'Language', 'Description', 'Cover']
#         rowList=[]
        b = self.getABook()
        book = Book()
        book.bookPath = b.bookPath
        book.bookImgName = b.bookImgName
        self.rowDict = dict()
        for idx, item in enumerate(rowList):
            print idx, item
            bitmap = wx.ArtProvider_GetBitmap(wx.ART_GO_BACK)
            self.reviewRow = ReviewRow()
            self.reviewRow.label = wx.StaticText(self.mainPanel, -1, item)
            self.reviewRow.copyRightToLeftButton = wx.BitmapButton(self.mainPanel, -1, bitmap, (10, 10), style=wx.BORDER_DEFAULT)    
            if item == 'Cover':
                self.reviewRow.leftText = PropertyPhotoPanel(self.mainPanel, book)
                self.reviewRow.rightText = PropertyPhotoPanel(self.mainPanel, book)
            else:
                
                self.reviewRow.leftText = wx.TextCtrl(self.mainPanel, -1, value="left" + item, size=(200, -1))
                self.reviewRow.rightText = wx.TextCtrl(self.mainPanel, -1, value="Right" + item, size=(200, -1))
                 
            self.rowDict[idx] = self.reviewRow
#         return self.rowDict

    
    def SetProperties(self):
        self.helptext.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Verdana"))
    def doLayout(self):
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        vBox = wx.BoxSizer(wx.VERTICAL)
        
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        
        leftBox = wx.BoxSizer(wx.VERTICAL)
        rightBox = wx.BoxSizer(wx.VERTICAL)
        hRow = wx.BoxSizer(wx.HORIZONTAL)
        centerBox = wx.BoxSizer(wx.VERTICAL) 
        centerBox.Add(wx.StaticText(self, -1, label=" "), 1, wx.EXPAND | wx.ALL, 5) 
        
        for key, value in self.rowDict.iteritems():
            print key
            hLeftRow = wx.BoxSizer(wx.HORIZONTAL)
            hRightRow = wx.BoxSizer(wx.HORIZONTAL)
            hLeftRow.Add(value.label, 3, wx.ALL | wx.EXPAND, 10)
            hLeftRow.Add(value.leftText, 7, wx.ALL | wx.EXPAND, 1)
            if value.label.GetLabel()=='Cover':
                hRightRow.Add(wx.StaticText(self, -1, label=" "), 1, wx.EXPAND | wx.UP,500 )
                hLeftRow.Add(wx.StaticText(self, -1, label=" "), 1, wx.EXPAND | wx.UP,500 )
            
            centerBox.Add(value.copyRightToLeftButton)
            
            hRightRow.Add(value.rightText, 1, wx.ALL | wx.EXPAND, 1)
            
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
        
        vBox.Add(vBoxSizer, 0, wx.ALL | wx.EXPAND, 0) 
        self.mainPanel.SetAutoLayout(True)
        self.mainPanel.SetSizer(vBox)
        vBox.Fit(self.mainPanel)
        vBox.SetSizeHints(self.mainPanel)
        mainsizer.Add(self.mainPanel, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(mainsizer)
        mainsizer.Layout()  
    
#----------------------------------------------------------------------
    def BindEvents(self):
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
    def onClose(self, event):
        self.Destroy()
        
        
    def getABook(self):
        books = FindingBook().findAllBooks()
        book = None
        for b in books:
            book = b
            break
        return book
class ReviewFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title='Review metadata', size=(600, 400))
        self.panel = ReviewMetadataPanel(self)          
        self.Show()
if __name__ == '__main__':
    app = wx.App(0)
    frame = ReviewFrame(None)
    app.MainLoop()  


# VBox
#     vBoxSizer
#         hBox
#             StaticBox
#             StaticBox
        
