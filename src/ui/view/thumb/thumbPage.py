import wx
import wx.grid
import os
import time
from src.ui.view.thumb import AboutBox
import wx.lib.agw.aui as aui
from src.ui.view.thumb.ThumbCrtl import ThumbnailCtrl, NativeImageHandler
from src.dao.BookDao import CreateDatabase
from src.static.constant import Workspace


class MainWindow(wx.Frame):

    def __init__(self, parent, title, *args, **kwargs):
        super(MainWindow, self).__init__(parent, title=title, size=wx.DisplaySize())
        self.frmPanel = wx.Panel(self)
#         global books
#         self.books = books
#         self.PhotoMaxSize = 240
#         self.frmPanel.SetBackgroundColour('sky blue')
        self.InitUI()

    def InitUI(self):
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.items = list()
        menubar = wx.MenuBar()
        topMenu = (
                   {'&File':[
                                 {'addBooks':['Add a book(s)', 'normal', 'addBooks.png'] },
                                 {'restart':['Restart', 'normal', 'restart.png']},
                                 {'quite':['&Quit\tCtrl+Q', 'normal', 'quite.png']}
                             ]
                    },
                   {'&Edit':[
                             {'undo':['Undo', 'normal', 'undo.png']},
                             {'redo':['Redo', 'normal', 'redo.png']},
                             {'editBook':['Edit a book info', 'normal', 'editBook.png']},
                             {'editBooks':['Edit a book info in bulk', 'normal', 'editBooks.png']}
                             ]
                    },
                   {'Preferences':[]
                    },
                   {'&View':[
                             {'statusBar':['Show status bar', 'check', 'statusBar.png']},
                             {'toolbar':['Show toolbar', 'check', 'toolbar.png']}
                             ]
                    },
                   {'&Help':[
                             {'aboutCalibre':['About Better Calibre', 'normal', 'aboutCalibre.png']}
                             ]
                    }
                   )

        i = 1
        j = 1
        for topLevel in topMenu:
            topLevelMenu = wx.Menu()  # Top level
            for k, topLevelItems in topLevel.iteritems():
                items = list()
                for topLevelItem in topLevelItems:
                    for child, childValue in topLevelItem.iteritems():
                        kind_value = None
                        if 'normal' == childValue[1]:
                            kind_value = wx.ITEM_NORMAL
                        elif 'radio' == childValue[1]:
                            kind_value = wx.ITEM_RADIO
                        elif 'check' == childValue[1]:
                            kind_value = wx.ITEM_CHECK
                        item = topLevelMenu.Append(i * 10 + j, childValue[0], childValue[0], kind=kind_value)
                        bmp = wx.ArtProvider_GetBitmap(wx.ART_FIND, wx.ART_OTHER, (16, 16))
#                         item.SetBitmap(bmp)
                        if 'check' == childValue[1]:
                            item.Check()

                        items.append(item)
                    j = j + 1
                self.items.append(items)
#                 topLevelMenu.Append(-1,childMenu)
            menubar.Append(topLevelMenu, k)
            i = i + 1


        self.Bind(wx.EVT_MENU, self.OnQuit, id=13)
        self.Bind(wx.EVT_MENU, self.OnRestart, id=12)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.items[4][0])

        self.Bind(wx.EVT_MENU, self.OnAdd, self.items[0][0])
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.items[3][0])
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.items[3][1])

        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        self.toolbar.AddLabelTool(1, '', wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16)))
        self.toolbar.Realize()

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        # Creating Grid Panel
        self.mainBookPanel = wx.Panel(self.frmPanel)


        self.searchPanel = wx.Panel(self.frmPanel, id=11)
        # add a bitmap on the left side
        self.searchTextPanel = wx.Panel(self.searchPanel, style=wx.SUNKEN_BORDER)
        bmp = wx.ArtProvider_GetBitmap(wx.ART_FIND, wx.ART_OTHER, (16, 16))
        self.staticbmp = wx.StaticBitmap(self.searchTextPanel, -1, bmp, pos=(1, 0))
#         w, h = self.staticbmp.GetSize()
#         self.searchText = wx.TextCtrl(self.searchTextPanel, id=100, style=wx.TE_PROCESS_ENTER | wx.NO_BORDER, value="", name=" Search: ", validator=SearchTextValidator())
        self.searchText = wx.TextCtrl(self.searchTextPanel, id=100, style=wx.TE_PROCESS_ENTER | wx.NO_BORDER, value="", name=" Search: ")
        self.searchText.SetToolTipString('Search your book here.')
        self.hbox_searchText = wx.BoxSizer (wx.HORIZONTAL)
        self.hbox_searchText.Add(self.staticbmp, flag=wx.CENTER)
        self.hbox_searchText.Add(self.searchText, proportion=1, flag=wx.CENTER)

        self.vbox_searchText = wx.BoxSizer(wx.VERTICAL)
        self.vbox_searchText.Add(self.hbox_searchText, proportion=1, flag=wx.EXPAND)
        self.searchTextPanel.SetSizerAndFit(self.vbox_searchText)

        self.searchLabel = wx.StaticText(self.searchPanel, -1, label="Search")
        self.searchButton = wx.Button(self.searchPanel, label="search")
        self.hboxSearchPanel = wx.BoxSizer (wx.HORIZONTAL)
        self.hboxSearchPanel.Add(self.searchLabel, flag=wx.CENTER)
        self.hboxSearchPanel.Add(self.searchTextPanel, 1, flag=wx.CENTER)
        self.hboxSearchPanel.Add(self.searchButton, flag=wx.CENTER)
        self.vBoxSearchPanel = wx.BoxSizer(wx.VERTICAL)
        self.vBoxSearchPanel.Add(self.hboxSearchPanel, proportion=1, flag=wx.EXPAND)
        self.searchPanel.SetSizerAndFit(self.vBoxSearchPanel)

        self.searchText.SetFocus()
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.EvtText)


        self.mainBookTab = MainBookTab(self.mainBookPanel)
        vbox_noteBook = wx.BoxSizer(wx.VERTICAL)
        vbox_noteBook.Add(self.mainBookTab, 1, wx.ALL | wx.EXPAND, 5)
#         vbox_noteBook.Add(self.gridPanel, 1, wx.ALL|wx.EXPAND, 5)
        self.mainBookPanel.SetSizer(vbox_noteBook)

        # Add them to sizer.
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(self.searchPanel, .1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(self.mainBookPanel, 9, wx.EXPAND | wx.ALL, 1)



        self.frmPanel.SetSizer(vBox)
        self.frmPanel.Layout()
        x, y = wx.DisplaySize()
        self.SetSize((x, y - 40))

        self.SetTitle('Better Calibre')
        self.Centre()
        self.Show(True)


    def gridActivity(self, bookName=None, books=None):
        print self.mainBookTab
        self.grid = self.mainBookTab.tabOne.grid
        print 'updating'

        self.grid.ForceRefresh()
        availableRows = self.grid.GetNumberRows()
        totalRows = len(books)
        self.grid.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.grid.ClearGrid()
        self.grid.ForceRefresh()
        try:
            self.grid.ClearGrid

            if totalRows > availableRows :
                try:
                    self.grid.AppendRows(totalRows - availableRows)
                except:
                    print 'one'

            elif totalRows < availableRows:
                print 'one_1'
                try:
                    self.grid.BeginBatch()
                    self.grid.DeleteRows(0, availableRows - totalRows, True)
                    self.grid.EndBatch()
                except:
                    print 'exception one_1'
            else:
                print 'one_2_'
                self.grid.DeleteRows(0, availableRows, True)
                self.grid.AppendRows(totalRows)
            rowNum = 0
    #         color = (100,100,255)
            color = 'light gray'
            attr = self.cellAttr = wx.grid.GridCellAttr()
            attr.SetBackgroundColour(color)
            print 'totalRows', totalRows
            print 'availableRows', availableRows

            for book in books:
                if rowNum % 2 == 0:
                    for i in range(10):
                        self.grid.SetAttr(rowNum, i, attr)
                self.grid.SetCellValue(rowNum, 0, book.bookName)
                self.grid.SetCellValue(rowNum, 1, book.authors[0].authorName)
                self.grid.SetCellValue(rowNum, 2, book.publisher)
                self.grid.SetCellValue(rowNum, 3, book.isbn_13)
                if book.fileSize:
                    self.grid.SetCellValue(rowNum, 4, book.fileSize)
                else:
                    self.grid.SetCellValue(rowNum, 4, '0')
                self.grid.SetCellValue(rowNum, 5, book.bookFormat)
                self.grid.SetCellValue(rowNum, 6, book.bookPath)
                rowNum = rowNum + 1
                self.SetStatusText('Done.')
        except:
            print 'somthing wrong with grid'

    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW, NewH)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()

    def OnAdd(self, event):
        """
        Browse for file

        """

        # This is how you pre-establish a file filter so that the dialog
        # only shows the extension(s) you want it to.
        wildcard = "PDF Book source (*.pdf)|*.pdf|" \
                    "TXT Book source (*.txt)|*.txt|"\
                    "All Book source (*.*)|*.*"

        dlg = wx.FileDialog(None, message="Choose a Python file", defaultDir=os.getcwd(),
                            defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns the file that was selected
            path = dlg.GetPath()

            # Open the file as read-only and slurp its content
            fid = open(path, 'rt')
            text = fid.read()
            fid.close()

            # Create the notebook page as a wx.TextCtrl and
            # add it as a page of the wx.Notebook
            text_ctrl = wx.TextCtrl(self.notebook, style=wx.TE_MULTILINE)
            text_ctrl.SetValue(text)

            filename = os.path.split(os.path.splitext(path)[0])[1]
            self.notebook.AddPage(text_ctrl, filename, select=True)

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()


    def ToggleStatusBar(self, e):

        if self.items[3][0].IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, e):

        if self.items[3][1].IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

    def OnQuit(self, event):
        self.Close()

    def OnRightDown(self, e):
        self.PopupMenu(MyPopupMenu(self), e.GetPosition())

    def OnRestart(self, event):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        self.Close()
        self.Destroy()
        self.Show(False)
        time.sleep(5)
        main()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()
        pass

    def OnFind(self, e):
        print 'finding'
        pass
        #----------------------------------------------------------------------



    def OnKeyDown(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()
            return

    def EvtText(self, event):
#         global books
#         engine = create_engine('sqlite:///calibre.sqlite', echo=True)
#         session = sessionmaker()
#         session.configure(bind=engine)
        bookName = event.GetString()
#         self.books = CreateDatabase().findByBookName(session, bookName)
        books = self.books
        self.thumbnail = self.mainBookTab.thumbnail
        self.thumbnail.ShowDir(books)
        self.gridActivity(bookName, self.books)
#         logger.info('EvtText: %s\n' % event.GetString())




########################################################################
class MainBookTab(aui.AuiNotebook):
    """
    Notebook class
    """
    DEFAULT_STYLE = aui.AUI_NB_MIDDLE_CLICK_CLOSE | \
                   aui.AUI_NB_CLOSE_ON_ACTIVE_TAB | \
                   aui.AUI_NB_SCROLL_BUTTONS | \
                   aui.AUI_NB_TAB_MOVE | \
                   aui.AUI_NB_TAB_SPLIT | \
                   aui.AUI_NB_TOP | \
                   wx.NO_BORDER
#----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        aui.AuiNotebook.__init__(self, parent=parent)
        self.default_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self.SetWindowStyleFlag(self.default_style)

        # Create the first tab and add it to the notebook
        self.gallery = TabPanel(self)


        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.thumbnail = ThumbnailCtrl(self.gallery, imagehandler=NativeImageHandler)
        self.thumbnail._scrolled.EnableToolTips(enable=True)

# # Todo
        books = list()
        print '1.---->', os.getcwd()
#         os.chdir('/home/vijay/Documents/Aptana_Workspace/util/src/dao')
        print '2.---->', os.getcwd()
#         session = CreateDatabase().creatingDatabase()
#         CreateDatabase().addingData()
#         books = CreateDatabase().findByBookName("python")
        books = CreateDatabase().findAllBook()

        if books != None:
            self.thumbnail.ShowDir(books)
        self.sizer.Add(self.thumbnail, 1, wx.EXPAND | wx.ALL, 10)
        self.gallery.SetSizer(self.sizer)

        self.tabOne = TabPanel(self)
        self.tabOne.addItems()
#         tabOne.SetBackgroundColour("Gray")
        bookImage = wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK , wx.ART_OTHER, wx.Size(16, 16))
        galleryImage = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, wx.Size(16, 16))
        self.AddPage(self.gallery, "Gallery", False, galleryImage)
        self.AddPage(self.tabOne, "Books", False, bookImage)
        style = self.DEFAULT_STYLE

        self.SetWindowStyleFlag(style)
        self.SetArtProvider(aui.AuiDefaultTabArt())
########################################################################
class TabPanel(wx.Panel):
    """
    This will be the first notebook tab
    """
    def _init_ctrls(self, prnt):
        wx.Panel.__init__(self, style=wx.TAB_TRAVERSAL | wx.NO_BORDER, name='', parent=prnt, pos=(0, 0), size=wx.Size(200, 100))

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)


    def addItems(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
#         self.grid = MainGrid(self)

#         vbox.Add(self.grid, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(vbox)
        pass

    def addHtml(self):
#         self.html = wx.html.HtmlWindow(self)
#         self.html.SetPage("Here is some <b>formatted</b> <i><u>text</u></i> "
#             "loaded from a <font color=\"red\">string</font>.")
        pass


class MyPopupMenu(wx.Menu):
    '''
    classdocs
    '''
    def __init__(self, parent):
        '''
        Constructor
        '''
        super(MyPopupMenu, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)

        cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.OnClose, cmi)


    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()


def main():
#     global books, frame
#     session = CreateDatabase().creatingDatabase()
# #     CreateDatabase().addingData(session)
#     books = CreateDatabase().findAllBook(session)
#     bookName = 'head'
#     books = CreateDatabase().findByBookName(session, bookName)
    if Workspace().libraryPath + os.sep + '_opal.sqlite':
        if os.stat(Workspace().libraryPath + os.sep + '_opal.sqlite').st_size == 0:
            c = CreateDatabase()
            c.creatingDatabase()
            c.addingData()
            print 'data loaded'
    app = wx.App(0)
    frame = MainWindow(None, "My Calibre")
    app.MainLoop()

if __name__ == '__main__':
    main()

