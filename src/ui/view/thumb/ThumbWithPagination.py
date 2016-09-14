
import wx
import os
from src.ui.view.thumb.ThumbCrtl import ThumbnailCtrl, NativeImageHandler
from src.dao.BookDao import CreateDatabase
from src.static.constant import Workspace

class MainWindow(wx.Frame):

    def __init__(self, parent, title, *args, **kwargs):
        super(MainWindow, self).__init__(parent, title=title, size=wx.DisplaySize())
        self.frmPanel = wx.Panel(self)

        self.initUI()
        
    def initUI(self):
        vBox = wx.BoxSizer(wx.VERTICAL)
        self.thumbnail = ThumbnailCtrl(self.frmPanel, imagehandler=NativeImageHandler)
        self.thumbnail._scrolled.EnableToolTips(enable=True)
#         toolbar = wx.ToolBar(self.thumbnail )
#         toolbar.AddLabelTool(1, '', wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16)))
#         toolbar.Realize()
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')
        books=list()
        books = CreateDatabase().findAllBook()

        if books != None:
            self.thumbnail.ShowDir(books)
#         vBox.Add(toolbar)
        vBox.Add(self.thumbnail, 1, wx.EXPAND | wx.ALL, 10)
        self.frmPanel.SetSizer(vBox)
        self.frmPanel.Layout()
        self.Show(True)
    
def main():

#     if Workspace().libraryPath + os.sep + '_opal.sqlite':
#         if os.stat(Workspace().libraryPath + os.sep + '_opal.sqlite').st_size == 0:
#             c = CreateDatabase()
#             c.creatingDatabase()
#             c.addingData()
#             print 'data loaded'
    app = wx.App(0)
    frame = MainWindow(None, "My Opal")
    app.MainLoop()

if __name__ == '__main__':
    main()