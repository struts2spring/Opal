'''
Created on 05-Dec-2015

@author: vijay
'''

__version__ = "1.0"


# from PIL import Image
import cStringIO
import os
import sys
import traceback
import wx
from wx.lib.agw import aui
import wx.grid
import wx.html
from wx.wizard import WizardPageSimple, Wizard
from wx.lib.filebrowsebutton import DirBrowseButton
from src.ui.view.opalview.property import BookPropertyFrame
import subprocess
import thread
from src.selenium_download.fullcircleMagazine import FullCircleMagazine
from src.ui.view.preference.OpalPreferences import OpalPreference
from src.static import OpalStartWorkspace
from src.static.OpalStartWorkspace import OpalStart
# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
try:
    from src.ui.view.kivy.main import PicturesApp
except:
    print 'error in loading kivy'
try:
    from src.dao.BookDao import CreateDatabase
except:
    print 'creating database error.'
from src.logic.AddingBook import AddBook
from src.logic.search_book import FindingBook
from src.static.constant import Workspace
from src.ui.view.SettingPanel import SettingsPanel
from src.ui.view.SizeReportCtrl import SizeReportCtrl
from src.ui.view.opalview import BookInfo
from src.ui.view.opalview.BookInfo import GenerateBookInfo
from src.ui.view.opalview.MyGrid import MegaGrid
from src.ui.view.opalview.SearchPanel import SearchPanel
from src.ui.view.opalview.otherWorkspace import WorkspacePanel, WorkspaceFrame
from src.ui.view.thumb.ThumbCrtl import NativeImageHandler, ThumbnailCtrl
from src.ui.view.online.thumb.searchOnline import SearchFrame
from src.audit.singletonLoggerLogging import Logger




try:
    import wx.html2
except:
    print 'error'
    
    
    
logger = Logger(__name__)   
logger.info('win logging init') 
#----------------------------------------------------------------------
global searchedBooks
searchedBooks = list()
ID_About = wx.NewId()
ID_Preferences = wx.NewId()
ID_Rest_view = wx.NewId()
ID_switchWorkspace = wx.NewId()
ID_otherWorkspace = wx.NewId()
ID_addBook = wx.NewId()
ID_deleteBook = wx.NewId()
ID_reLoadDatabase = wx.NewId()
ID_search = wx.NewId()
ID_editMetadata = wx.NewId()
ID_cover_flow = wx.NewId()
ID_FullCircle = wx.NewId()
print '------other id --------', ID_otherWorkspace

# Define File Drop Target class
class FileDropTarget(wx.FileDropTarget):
    """ This object implements Drop Target functionality for Files """
    def __init__(self, obj):
        """ Initialize the Drop Target, passing in the Object Reference to
            indicate what should receive the dropped files """
        # Initialize the wxFileDropTarget Object
        wx.FileDropTarget.__init__(self)
        # Store the Object Reference for dropped files
        self.obj = obj
    
    def OnDropFiles(self, x, y, filenames):
        """ Implement File Drop """
        # For Demo purposes, this function appends a list of the files dropped at the end of the widget's text
        # Move Insertion Point to the end of the widget's text
        print 'OnDropFiles'
#         self.obj.SetInsertionPointEnd()
        # append a list of the file names dropped
        print ("%d file(s) dropped at %d, %d:\n" % (len(filenames), x, y))
        for file in filenames:
            self.selectedFilePath = file
            print ('           %s\n' % file)
            if file:
                AddBook().addingBookToWorkspace(file)
            print self
        print 'drop book completed.'
        print self
        text = self.obj.searchCtrlPanel.searchCtrl.GetValue()
        self.obj.searchCtrlPanel.doSearch(text)
#         self.obj.WriteText('\n')


class MainFrame(wx.Frame):

    def __init__(self, parent):
        title = "Opal"
        size = wx.DefaultSize
        style = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE | wx.SUNKEN_BORDER
#         wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, style=style)
        print '1----------------------->'
        image = wx.Image(os.path.join(Workspace().appPath, "images", "Library-icon.png"), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(image)
        # set frame icon
        self.SetIcon(icon)
        
        
        
        if not os.path.exists(Workspace().libraryPath):
            self.createWizard()
        self.createDatabase = CreateDatabase()
#         self.creatingDatabase()
        
        self.books = list()
        self.thumbnail = None
        self.fileDropTarget = FileDropTarget(self)
#         self.grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250),wx.NO_BORDER | wx.WANTS_CHARS)

        self._mgr = aui.AuiManager()
        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self)
        
        # set up default notebook style
        self._notebook_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self._notebook_theme = 0
        # Attributes
        self._textCount = 1
        self._transparency = 255
        self._snapped = False
        self._custom_pane_buttons = False
        self._custom_tab_buttons = False
        self._pane_icons = False
        self._veto_tree = self._veto_text = False  
        print '1----------------------->', os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        


        self.BuildPanes()
        self.CreateMenuBar()
        self.BindEvents()
        self.buildStatusBar()
        
    def BuildPanes(self):   
        # min size for the frame itself isn't completely done.
        # see the end up AuiManager.Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))        
        # prepare a few custom overflow elements for the toolbars' overflow buttons

        prepend_items, append_items = [], []
        # add the toolbars to the manager
        tb1 = wx.ToolBar(self, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_TEXT)
        tb1.SetToolBitmapSize(wx.Size(24, 24))
        tb1.AddLabelTool(id=ID_otherWorkspace, label="Workspace Home", shortHelp="Home" , bitmap=wx.ArtProvider_GetBitmap(wx.ART_GO_HOME))
        tb1.AddSeparator()
        tb1.AddLabelTool(id=ID_search, label="Search", shortHelp="Search" , bitmap=wx.ArtProvider_GetBitmap(wx.ART_FIND))
        tb1.AddLabelTool(id=ID_editMetadata, label="Edit metadata", shortHelp="Edit metadata", bitmap=wx.ArtProvider_GetBitmap(wx.ART_WARNING))
        tb1.AddLabelTool(id=ID_addBook, label="Add book", shortHelp="Add book", bitmap=wx.Bitmap(os.path.join(Workspace().appPath, "images", "add_book.png")))
        tb1.AddLabelTool(id=ID_deleteBook, label="Delete book", shortHelp="Delete book", bitmap=wx.ArtProvider_GetBitmap(wx.ART_DELETE))
#         tb1.AddLabelTool(id=ID_deleteBook, label="Delete book", shortHelp="Delete book", bitmap=wx.Bitmap(os.path.join(Workspace().appPath, "images", "delete_book.png")))
        tb1.AddLabelTool(id=ID_reLoadDatabase, label="Reload database", shortHelp="Reload database", bitmap=wx.Bitmap(os.path.join(Workspace().appPath, "images", "database_refresh.png")))
        tb1.AddLabelTool(id=ID_Rest_view, label="Reset View", shortHelp="Reset View", bitmap=wx.ArtProvider_GetBitmap(wx.ART_LIST_VIEW))
        tb1.AddLabelTool(id=ID_cover_flow, label="Cover Flow", shortHelp="Cover Flow", bitmap=wx.ArtProvider_GetBitmap(wx.ART_HELP_BOOK))
        tb1.AddLabelTool(id=ID_FullCircle, label="Full Circle Magazine", shortHelp="download Full Circle Magazine", bitmap=wx.Bitmap(os.path.join(Workspace().appPath, "images", "fullcircle.png")))
        tb1.AddLabelTool(id=ID_Preferences, label="Preferences", shortHelp="Preferences", bitmap=wx.ArtProvider_GetBitmap(wx.ART_EXECUTABLE_FILE))
        tb1.Realize()

        self._mgr.AddPane(tb1, aui.AuiPaneInfo().Name("tb1").Caption("Big Toolbar").ToolbarPane().Top().LeftDockable(True).RightDockable(False))

        # add a bunch of panes
        bookInfoPan = aui.AuiPaneInfo().Name("bookInfo").Caption("Text Pane").Right().Layer(1).Position(1).CloseButton(True).MaximizeButton(True).MinimizeButton(True).PaneBorder(True)
        self._mgr.AddPane(self.CreateTextCtrl(), bookInfoPan)
#         self._mgr.AddPane(SettingsPanel(self, self), wx.aui.AuiPaneInfo().Name("settings").Caption("Dock Manager Settings").Dockable(True).Float().Hide().CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.searchCtrl(), aui.AuiPaneInfo().Name("searchCtrl").Top().CaptionVisible(False).CloseButton(False).Show())
#         self._mgr.AddPane(self.CreateGrid(), wx.aui.AuiPaneInfo().Name("grid_content").CenterPane().CloseButton(True).Show())
        self._mgr.AddPane(self.CreateGrid(), aui.AuiPaneInfo().Name("grid_content").Caption("Grid").Center().CloseButton(True).MaximizeButton(True).LeftDockable(True).MinimizeButton(True).PaneBorder(True))
        
        thumbInfo = aui.AuiPaneInfo().Name("test1").Caption("Thumb book").Center().Dockable(True).Movable(True).MaximizeButton(True).MinimizeButton(True).PinButton(True).CloseButton(True).Position(0).PaneBorder(True)
        self._mgr.AddPane(self.CreateThumbCtrl(), thumbInfo)
#         self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().Name("tree_content").CenterPane().Hide())

#         self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().Name("sizereport_content").CenterPane().Show())

#         self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().Name("text_content").CenterPane().Show())
        html_content = aui.AuiPaneInfo().Caption("Book Information").Name("html_content").Right().Dockable(True).Layer(1).Position(1).CloseButton(True).MaximizeButton(True).MinimizeButton(True)
        self._mgr.AddPane(self.CreateHTMLCtrl(), html_content)

#         perspective_all = self._mgr.SavePerspective()
        self.perspective_default = self._mgr.SavePerspective()
        
        perspective_default = self._mgr.SavePerspective()
        # make some default perspectives
        perspective_all = self._mgr.SavePerspective()
        self._perspectives = []
        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)
        
        all_panes = self._mgr.GetAllPanes()
        for pane in all_panes:
            if not pane.IsToolbar():
#                 pane.Hide()
                pane.Show()
                
        perspective_default = self._mgr.SavePerspective()

        self._perspectives = []
        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)

        self._nb_perspectives = []


        # "commit" all changes made to FrameManager
        self._mgr.Update()        
        
    def CreateMenuBar(self):
        # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
#         qmi = wx.MenuItem(file_menu, wx.ID_EXIT, '&Quit\tCtrl+Q')
#         qmi.SetBitmap(wx.Bitmap('/home/vijay/Documents/Aptana_Workspace/util/src/ui/view/opalview/images/exit-16.png'))
        switchWorkspaceMenu = wx.Menu()

        switchWorkspaceMenu.Append(ID_otherWorkspace, 'Other...')
#         file_menu.AppendMenu(wx.ID_ANY, 'I&mport', switchWorkspaceMenu)
        file_menu.AppendMenu(ID_switchWorkspace, 'Switch Workspace', switchWorkspaceMenu)
        file_menu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q')

        view_menu = wx.Menu()
        view_menu.Append(ID_Rest_view, "Reset view to default")
        windowMenu = wx.Menu()
        windowMenu.Append(ID_Preferences, "Preference")
        
        help_menu = wx.Menu()

        help_menu.Append(ID_About, "&About...")


        mb.Append(file_menu, "File")
        mb.Append(view_menu, "View")
        mb.Append(windowMenu, "Window")  
        mb.Append(help_menu, "Help")  
        self.SetMenuBar(mb) 
    def BindEvents(self):
        # Show How To Use The Closing Panes Event
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)  
        
        
        
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)
        self.Bind(wx.EVT_MENU, self.OnRestView, id=ID_Rest_view)
        self.Bind(wx.EVT_MENU, self.OnCoverFlow, id=ID_cover_flow)
        self.Bind(wx.EVT_MENU, self.OnFullCircle, id=ID_FullCircle)
        

        self.Bind(wx.EVT_MENU, self.onOtherWorkspace, id=ID_otherWorkspace)
        self.Bind(wx.EVT_MENU, self.onAddBookToWorkspace, id=ID_addBook)
        self.Bind(wx.EVT_MENU, self.onDeleteBookToWorkspace, id=ID_deleteBook)
        self.Bind(wx.EVT_MENU, self.onReLoadDatabaseToWorkspace, id=ID_reLoadDatabase)
        self.Bind(wx.EVT_MENU, self.onSearch, id=ID_search)
        self.Bind(wx.EVT_MENU, self.onEditMetadata, id=ID_editMetadata)
        self.Bind(wx.EVT_MENU, self.OnRestView, id=ID_Rest_view)
        self.Bind(wx.EVT_MENU, self.OnRestView, id=ID_Rest_view)
        self.Bind(wx.EVT_MENU, self.OnPreferences, id=ID_Preferences)
        
                       
    def buildStatusBar(self):
        
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Opal version 0.1", 0)
        findingBook = FindingBook()
        totalBookCount = findingBook.countAllBooks()
        selectedBooks = '0'
        if self.books:
            selectedBooks = str(len(self.books))
#         if  totalBookCount == None :
#             totalBookCount = 0
        
        self.statusbar.SetStatusText("selected : " + selectedBooks + " of " + str(totalBookCount), 1)
#         self.statusbar.SetStatusText("Number of books :" + str(len(self.books)), 1)
    def creatingDatabase(self):
        if not os.path.exists(Workspace().libraryPath):
            os.mkdir(Workspace().libraryPath)
        os.chdir(Workspace().libraryPath)
        listOfDir = os.listdir(Workspace().libraryPath)
        isDatabase = False
        for sName in listOfDir:
            if ("_opal.sqlite" in str(sName)) and (os.stat(Workspace().libraryPath + os.sep + '_opal.sqlite').st_size != 0):
                print sName
                isDatabase = True
        if not  isDatabase:
            self.createDatabase .addingData()
     
    def onEditMetadata(self, event):
        print 'onEditMetadata'
        if self.thumbnail._scrolled._selected != None:
            book = self.thumbnail._scrolled._items[self.thumbnail._scrolled._selected].book
#             frame = BookPropertyFrame(parent=None,book)
            frame = BookPropertyFrame(None, book)
    def onSearch(self, event):
        print 'onSearch'
        frame = SearchFrame(parent=None)
        
    def OnClose(self, event):
        logger.info('win OnClose')
        print 'OnClose'
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()

    def OnExit(self, event):
        logger.info('win OnClose')
        print 'OnExit'
        self.Close()


    def OnAbout(self, event):

        msg = "Opal\n" + \
              "An advanced book management library \n" + \
              "(c) Copyright 2005-2006,All rights reserved. \n original \"BSD License \" \n" + \
              "version : 0.1\n" + \
              "build : 0.1\n"
        dlg = wx.MessageDialog(self, msg, "About Opal", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPreferences(self, event):
        print 'OnPreferences'
        # frame1 = OpalPreferenceFrames(None)
        frame1 = OpalPreference(None, "Opal preferences")

    def OnRestView(self, event):
        print 'OnResetView'
        self._mgr.LoadPerspective(self.perspective_default)
        
    def OnFullCircle(self, event):
        print 'OnFullCircle'
        fullCircleMagazine = FullCircleMagazine()
        fullCircleMagazine.startDownload()
        
    def OnCoverFlow(self, event):
        print 'OnCoverFlow'
        try:
            thread.start_new_thread(self.startShell, (1,))
#             MyApp().run()
        except:
            print "Error: unable to start thread"
#         exit_code = call("python3 2.py", shell=True)
#         exit_code = subprocess.call("python3 2.py", shell=False)
#         cmd = "python3 2.py"
#         p = subprocess.Popen(cmd, shell=False, bufsize=1024, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#         pid = os.popen(cmd)
#         print pid
#         print exit_code
#         MyApp().run()
#         self._mgr.LoadPerspective(self.perspective_default)
    def startShell(self, a):
#         books = FindingBook().findAllBooks()
        self.picture = PicturesApp()
        self.picture.setValue(books=self.books)
        self.picture.run()
#         PicturesApp(self.books).run()
#         from subprocess import call
#         os.chdir('/docs/github/Opal/src/ui/view/kivy')
#         print '-----1----1------','---> ',os.getcwd()
#         cmd ='bsh /docs/github/Opal/src/ui/view/kivy/shell.sh'
#         subprocess.call(['./shell.sh']) 
        
    def searchCtrl(self):
        self.searchCtrlPanel = SearchPanel(self)
#         self.searchCtrl.SetToolTip(wx.ToolTip('Search'))
#         self.searchCtrl.Bind(wx.EVT_TEXT, self.OnTextEntered)
        return self.searchCtrlPanel
#     def OnTextEntered(self, event):
#         text = self.searchCtrl.GetValue()
# #         self.doSearch(text)
#         print 'OnTextEntered', text

    def GetDockArt(self):
        return self._mgr.GetArtProvider()


    def DoUpdate(self):
        self._mgr.Update()


    def OnEraseBackground(self, event):
        event.Skip()


    def OnSize(self, event):
        event.Skip()

    def OnPaneClose(self, event):
        caption = event.GetPane().caption
        print caption

        if caption in ["Tree Pane", "Dock Manager Settings", "Fixed Pane"]:
            msg = "Are You Sure You Want To Close This Pane?"
            dlg = wx.MessageDialog(self, msg, "AUI Question", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                event.Veto()
            dlg.Destroy()

    def CreateThumbCtrl(self):
#         ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition, wx.Size(width, height), self._mgr)
#         self.books=FindingBook().findAllBooks()

        if not self.thumbnail:
            self.thumbnail = ThumbnailCtrl(self, imagehandler=NativeImageHandler)
            self.thumbnail._scrolled.EnableToolTips(enable=True)
            self.thumbnail.SetDropTarget(self.fileDropTarget)

        # # Todo
#         print 'before', len(self.books)
#         self.books=list()
#         findingBook=FindingBook()
#         books=findingBook.searchingBook(text)
#         self.fileDropTarget = FileDropTarget(self)
        
#         print 'CreateThumbCtrl', len(self.books)
        try:
            self.thumbnail.ShowDir(self.books)
        except:
            traceback.print_exc()
        return self.thumbnail

    def CreateTextCtrl(self):
        text = ("This is text box %d") % (1)
        return wx.TextCtrl(self, -1, text, wx.Point(0, 0), wx.Size(600, 400), wx.NO_BORDER | wx.TE_MULTILINE)

    def CreateHTMLCtrl(self):
#         self.ctrl = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(600, 400))
#         if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
#             self.ctrl.SetStandardFonts()
#         self.ctrl.SetPage(self.GetIntroText())
        if sys.platform == 'win32':
            self.browser = wx.html2.WebView.New(self)
            self.browser.LoadURL("C:\\Users\\vijay\\workspace\\3d_cover_flow\\WebContent\\3D-Cover-Flip-Animations-with-jQuery-CSS3-Transforms-Cover3D\\indexSimpleDemo.html")
        else:
            self.browser = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(600, 400))
            if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
                self.browser.SetStandardFonts()
        self.browser.SetDropTarget(self.fileDropTarget)
        return self.browser

    def CreateGrid(self):
        try:
#             books=FindingBook().searchingBook('flex')
#             self.LoadingBooks()

            opalStart = OpalStart()
            jsonFileStr = opalStart.readWorkspace()
            startObject = opalStart.jsonToObject(jsonFileStr)
            print startObject.workspace[0]['Preference']['recordPerPage']
            recordPerPage = startObject.workspace[0]['Preference']['recordPerPage']
            
            self.books = FindingBook().findAllBooks(pageSize=recordPerPage)
#             self.books=FindingBook().findAllBooks()
            colnames = ['id', 'bookName', 'bookFormat', 'authors', 'bookPath', 'isbn_13', 'isbn_10', 'inLanguage', 'series', 'rating', 'subTitle', 'uuid', 'publishedOn', 'editionNo', 'numberOfPages', 'hasCover', 'fileSize', 'publisher', 'hasCode', 'createdOn', 'dimension', 'bookDescription', 'customerReview']
            data = []
            bookId_rowNo_dict = {}
            
            if self.books:
                noOfBooks = len(self.books)
                print 'CreateGrid: noOfBooks:', noOfBooks
                for i in range(noOfBooks):
                    d = {}
                    
                    data.append((str(i), self.dicForGrid(self.books[i])))
                    bookId_rowNo_dict[self.books[i].id] = i
            self.grid = MegaGrid(self, data, colnames)
            self.grid.bookId_rowNo_dict = bookId_rowNo_dict
            self.grid.Reset()
        except:
            print 'error in grid', traceback.print_exc()
#         self.grid.books=self.books

        self.grid.SetDropTarget(self.fileDropTarget)
        return self.grid

    def dicForGrid(self, book):
        '''
        this method has been used for constructing grid data.
        '''
        dicForBook = book.__dict__
        authorsName = list()
        for author in book.authors:
#             print author.__dict__
            authorsName.append(author.authorName)
        dicForBook['authorName'] = (" \n").join(authorsName)
        
        return dicForBook
        
    def GetIntroText(self):



        return overview

    def onReLoadDatabaseToWorkspace(self, event):
        print 'onReLoadDatabaseToWorkspace'
        self.reloadingDatabase()
        
    def reloadingDatabase(self):
        self.createDatabase.creatingDatabase()
        self.createDatabase.addingData()
        text = self.searchCtrlPanel.searchCtrl.GetValue()
        self.searchCtrlPanel.doSearch(text)

    def onDeleteBookToWorkspace(self, event):
        print 'onDeleteBookToWorkspace'
        pass
    def onAddBookToWorkspace(self, event):
        print 'onAddBookToWorkspace'
        print ("CWD: %s\n" % os.getcwd())

        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'open' dialog, and allows multitple
        # file selections as well.
        #
        # Finally, if the directory is changed in the process of getting files, this
        # dialog is set up to change the current working directory to the path chosen.
        dlg = wx.FileDialog(
            self, message="Select a book",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()

            print ('You selected %d files:' % len(paths))

            for path in paths:
                self.selectedFilePath = path
                print ('           %s\n' % path)
                AddBook().addingBookToWorkspace(path)
                text = self.searchCtrlPanel.searchCtrl.GetValue()
                self.searchCtrlPanel.doSearch(text)

        # Compare this with the debug above; did we change working dirs?
        print ("CWD: %s\n" % os.getcwd())

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()

    def onOtherWorkspace(self, event):
        '''
        This method need to be called in following scenario.
        1. if there is no opal_start.json.
        2. if file present and no valid path.
        '''
        print 'onOtherWorkspace'
#         panel = WorkspacePanel(self)
        win = WorkspaceFrame(self, -1, "Workspace Launcher", size=(470, 290), style=wx.DEFAULT_FRAME_STYLE)
        win.Show(True)


    def LoadingBooks(self):
        self.createDatabase.addingData()
        
        
    def createWizard(self):
        # Create the wizard and the pages
        wizard = Wizard(self, -1, "Opal welcome wizard", wx.EmptyBitmap(200, 200))
        page1 = TitledPage(wizard, "Welcome to Opal")
        page2 = TitledPage(wizard, "Page 2")
        page3 = TitledPage(wizard, "Page 3")
        page4 = TitledPage(wizard, "Page 4")
        self.page1 = page1
        self.page1 = page1


        
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        lable = wx.StaticText(page1, -1, "Choose your language:")
        choice = wx.Choice(page1, -1, (0, 0), choices=['English'])
        choice.SetSelection(0)
        vbox.Add(lable, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        vbox.Add(choice, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        page1.sizer.Add(vbox)
#         vbox = wx.BoxSizer(wx.HORIZONTAL)
#         t1 = wx.TextCtrl(page1, -1, "Test it out and see", size=(125, -1))
#         vbox.Add(t1, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
#         page1.sizer.Add(vbox)

        page1.sizer.Add(wx.StaticText(page1, -1, """
            Choose a location of your workspace. 
            When you add books to Opal, they will be copied here. 
            Use an empty folder for a new Opal workspace."""), 0, wx.ALIGN_LEFT | wx.ALL, 1)
        dbb = DirBrowseButton(page1, -1, size=(450, -1), changeCallback=self.dbbCallback)
        dbb.SetFocus()
        dbb.SetLabel("Book Library Location")
        dbb.SetHelpText('Please set your default workspace location.')
        dbb.textControl.SetValue(Workspace().path)
        
        page1.sizer.Add(dbb , 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        wizard.FitToPage(page1)

        # Use the convenience Chain function to connect the pages
        WizardPageSimple.Chain(page1, page2)
#         WizardPageSimple.Chain(page2, page3)
#         WizardPageSimple.Chain(page3, page4)

        wizard.GetPageAreaSizer().Add(page1)
        if wizard.RunWizard(page1):
            pass
#             print '------------',wx.MessageBox("Wizard completed successfully", "That's all folks!")
#         else:
#             print '------------',wx.MessageBox("Wizard was cancelled", "That's all folks!")

    def dbbCallback(self, evt):
        print('DirBrowseButton: %s\n' % evt.GetString())
        if evt.GetString():  
            Workspace().path = evt.GetString() 
             

#----------------------------------------------------------------------



class TitledPage(WizardPageSimple):
    def __init__(self, parent, title):
        WizardPageSimple.__init__(self, parent)
        self.sizer = self.makePageTitle(title)        

    def makePageTitle(self, header=None):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        title = wx.StaticText(self, -1, header)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        subTitle = wx.StaticText(self, -1, "World's easiest way to organize ebook.")
        
        sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(subTitle, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        return sizer    
        
#---------------------------------------------------------------------------

# This is how you pre-establish a file filter so that the dialog
# only shows the extension(s) you want it to.
wildcard = "All files (*.*)|*.*|"\
            "PDF Books (*.pdf)|*.pdf|"     \
           "EPUB Books (*.epub)|*.epub|" \
           "Text Books (*.txt)|*.txt|"    \
           "Comics (*.cbz)|*.cbz"
#            "All files (*.*)|*.*"

overview = '''
    <!DOCTYPE html>
<html>
    <head>
        <style>
            div.img {
                height: auto;
                width: auto;
                float: left;
            }

            div.img img {
                display: inline;
            }

            div.img a:hover img {
            }

            div.desc {
                font-weight: normal;
                width: 120px;
            }
        </style>
    </head>
    <body>
    this is a test message.
            <a target="_blank" href="klematis_big.htm"><img src="/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/1/a_peek_at_computer_electronics.jpg" alt="Professional Java for Web Applications" title="Professional Java for Web Applications" width="200" ></a>

    </body>
</html>

    '''

if __name__ == "__main__":

    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()
