from src.logic.search_book import FindingBook
import wx
from wx.lib.expando import ExpandoTextCtrl
import logging

logger = logging.getLogger('extensive')

class Window(wx.App):
    def __init__(self, book=None):
        wx.App.__init__(self)
        self.init_ui(book=book)
        self.mainWindow.Show()

    def init_ui(self, book=None):
        self.mainWindow = wx.Frame(None)
        self.mainWindow.SetSize((800, 510))
        panel = PropertyPanel(self.mainWindow, book)
        
class PropertyPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        bookNameLabel = wx.StaticText(self, -1, "Title:") 
        bookName = wx.TextCtrl(self, -1, "", size=(150, -1));
        
        booShortkNameLabel = wx.StaticText(self, -1, "Short Title:") 
        bookShortName = ExpandoTextCtrl(self, -1, "", size=(150, -1));

        authorsLabel = wx.StaticText(self, -1, "Authors:") 
        authorName = wx.TextCtrl(self, -1, "", size=(50, -1));
        
        numberOfPagesLabel = wx.StaticText(self, -1, "Number of pages:") 
        numberOfPages = wx.TextCtrl(self, -1, "", size=(70, -1));
        
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(bookNameLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox1.Add(bookName, 0, wx.EXPAND|wx.ALL)
        
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2.Add(authorsLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox2.Add(authorName, 0, wx.EXPAND|wx.ALL)
        
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3.Add(booShortkNameLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox3.Add(bookShortName, 0, wx.EXPAND|wx.ALL)
        
        hBox4 = wx.BoxSizer(wx.HORIZONTAL)
        hBox4.Add(numberOfPagesLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox4.Add(numberOfPages, 0, wx.EXPAND|wx.ALL)
        
        vBox.Add(hBox1, 1, wx.EXPAND|wx.ALL, 1)
        vBox.Add(hBox2, 1, wx.EXPAND|wx.ALL, 1)
        vBox.Add(hBox3, 1, wx.EXPAND|wx.ALL, 1)
        vBox.Add(hBox4, 1, wx.EXPAND|wx.ALL, 1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox)
        self.SetSizer(sizer)
if __name__ == "__main__":
    books = FindingBook().findAllBooks()
    book = None
    for b in books:
        book = b
        break
    print book
    app = Window(book=book)
    app.MainLoop()
