
import wx
from src.ui.view.thumb.ThumbCrtl import NativeImageHandler, ThumbnailCtrl
import os
import requests
import book
from book import Book, VolumeInfo
import urllib2
import urllib
import shutil

#----------------------------------------------------------------------
sampleList = ['google book', 'amazon book', 'IT ebook', 'Tubebl', 'Lit2go', 'Project Gutenberg',
                      'ePubBud', 'Scribd', 'ManyBooks', 'Obooko', 'Wattpad', 'Ebookee',
                      'ShareBookFree', 'FreeBookSpot', 'Bookyards', 'FreeBooks4Doctors', 'Smashwords',
                      'BookBoon', 'Dailylit', 'Free-eBooks', 'PDFGeni', 'E-Books Directory', 'issuu', 'WikiBooks']

class SearchBookPanel(wx.Panel):
    '''
    This class searches online book metadata.
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        print 'SearchBookPanel'
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'opalview', "images"))

        image = wx.Image('pdf.png', wx.BITMAP_TYPE_ANY)
        img = image.Scale(18, 18)
        imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))

        self.search = wx.SearchCtrl(self, size=wx.DefaultSize, style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        self.search.SetMenu(self.MakeMenu())
        
        self.thumbnail = ThumbnailCtrl(self, imagehandler=NativeImageHandler)
#         self.thumbnail.showdir
# ## start of checklist
        lb = wx.CheckListBox(self, -1, (0, 0), wx.DefaultSize, sampleList)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBox, lb)
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, lb)
        lb.SetSelection(0)
        self.lb = lb

        lb.Bind(wx.EVT_RIGHT_DOWN, self.OnDoHitTest)
        
        pos = lb.GetPosition().x + lb.GetSize().width + 25
        btn = wx.Button(self, -1, "Test SetString", (pos, 50))
        self.Bind(wx.EVT_BUTTON, self.OnTestButton, btn)
# ## end of checklist

        vbox_1 = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox_1 = wx.BoxSizer(wx.HORIZONTAL)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((15, 15))
        hbox.Add(imageBitmap, 0, wx.ALL, 17)
        vbox.Add(self.search, 0, wx.EXPAND, 15)
#         vbox.Add(self.thumbnail, 1, wx.EXPAND | wx.ALL, 10)
        hbox.Add(vbox, 9, wx.EXPAND | wx.RIGHT, 0)
        
        vbox_1.Add(hbox, 1, wx.EXPAND | wx.RIGHT, 0)
        hbox_1.Add(self.lb, 2, wx.EXPAND | wx.ALL, 0)
        hbox_1.Add(self.thumbnail, 8, wx.EXPAND | wx.ALL, 0)
        vbox_1.Add(hbox_1, 9, wx.EXPAND | wx.RIGHT, 0)
        
        self.SetSizerAndFit(vbox_1, True)



        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.search)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search)


    def OnToggleSearchButton(self, evt):
        self.search.ShowSearchButton(evt.GetInt())
            
    def OnToggleCancelButton(self, evt):
        self.search.ShowCancelButton(evt.GetInt())
        
    def OnToggleSearchMenu(self, evt):
        if evt.GetInt():
            self.search.SetMenu(self.MakeMenu())
        else:
            self.search.SetMenu(None)


    def OnSearch(self, evt):
        print("OnSearch")
            
    def OnCancel(self, evt):
        print("OnCancel")

    def OnDoSearch(self, evt):
        print("OnDoSearch: " + self.search.GetValue())
#         listOfBooks = self.doGoogleSearch()
        listOfBooks=list()
        self.doAmazonBookSerach()
        
        print len(listOfBooks)
        
        self.thumbnail.ShowDir(listOfBooks)
        
    def doAmazonBookSerach(self):
        searchUrl='http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Ddigital-text&field-keywords='+ self.search.GetValue()
        r=requests.get(searchUrl)
        
        
        pass
    def doGoogleSearch(self):
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + self.search.GetValue())
        json_data = r.json()
        items = json_data['items']
        listOfBooks = []
        for x in items:
        #     print x.keys()
            b = Book(x)
            volumeInfo = VolumeInfo(b['volumeInfo'])
            b.bookName = volumeInfo.title
#                volumeInfo.imageLinks['thumbnail']
            
            if volumeInfo.has_key('imageLinks'):
                url = str(volumeInfo.imageLinks['thumbnail'])
            else:
                url = "https://books.google.co.in/googlebooks/images/no_cover_thumb.gif"
                
            path = os.path.join('/tmp', 'img')
#             os.mkdir(tmp_path)
#             path = os.path.dirname(__file__) + os.sep + 'tmp'
            print path
            if not os.path.exists(path):
                os.mkdir(path)
            b.localImagePath = path 
#             + os.sep + b.id + '.jpeg'
            b.imageFileName = b.id + '.jpeg'
            if not os.path.exists(os.path.join(b.localImagePath, b.imageFileName)):
                os.chdir(path)
                print 'writing file'
                with open(path + os.sep + b.id + '.jpeg', 'wb') as f:
                    f.write(urllib2.urlopen(url).read())
            b.volumeInfo = volumeInfo
            b.bookPath = None
            listOfBooks.append(b)
        return listOfBooks

    def MakeMenu(self):
        menu = wx.Menu()
        item = menu.Append(-1, "Recent Searches")
        item.Enable(False)
        for txt in [ "Google Books",
                     "Amazon Books",
                     "Find Books",
                     "and bind EVT_MENU to",
                     "catch their selections" ]:
            menu.Append(-1, txt)
        return menu
         
    def EvtListBox(self, event):
        print('EvtListBox: %s\n' % event.GetString())

    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        label = self.lb.GetString(index)
        status = 'un'
        if self.lb.IsChecked(index):
            status = ''
        print('Box %s is %schecked \n' % (label, status))
        self.lb.SetSelection(index)  # so that (un)checking also selects (moves the highlight)
        
    def OnTestButton(self, evt):
        self.lb.SetString(4, "FUBAR")

    def OnDoHitTest(self, evt):
        item = self.lb.HitTest(evt.GetPosition())
        print("HitTest: %d\n" % item)
#----------------------------------------------------------------------
class SearchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title='Search Book', size=(600, 400))
        self.panel = SearchBookPanel(self)
        self.Show()
#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.SearchCtrl</center></h2>
</body></html>
"""



if __name__ == '__main__':
    app = wx.App(0)
    frame = SearchFrame(None)
    app.MainLoop()  
