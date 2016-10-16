from src.logic.search_book import FindingBook
import wx
from wx.lib.expando import ExpandoTextCtrl


class Window(wx.App):
    def __init__(self, book=None):
        wx.App.__init__(self)
        self.init_ui()
        self.mainWindow.Show()

    def init_ui(self):
        self.mainWindow = wx.Frame(None)
        self.mainWindow.SetSize((800, 510))
        panel = GeneralPreferencePanel(self.mainWindow)
        
class GeneralPreferencePanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        self.st = wx.StaticLine(self, wx.ID_ANY)
        # Make and layout the controls
        fs = self.GetFont().GetPointSize()
        bf = wx.Font(fs+4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs+2, wx.SWISS, wx.NORMAL, wx.NORMAL)
        label=''
        if kw.has_key('preferenceName'):
            label=kw['preferenceName']
        self.header = wx.StaticText(self, -1, label)
        self.header.SetFont(bf)
        vBox.Add(self.header, 0, wx.ALL | wx.EXPAND, 5)
        vBox.Add(self.st, 0, wx.ALL | wx.EXPAND, 5)
        
        self.systemTray = wx.CheckBox(self, -1, "Enable system tray icon (needs restart)", style=wx.ALIGN_RIGHT)
        
        sampleList = ['Title', 'authors', 'comment', 'publisher', 'rating']

        self.fieldsUnderCoverLabel=wx.StaticText(self, -1, "Field to show under cover.", (45, 15))

        lb = wx.CheckListBox(self, -1, (80, 50), wx.DefaultSize, sampleList)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBox, lb)
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, lb)
        lb.SetSelection(0)
        self.lb = lb
#         self.workspacePathLabel = wx.StaticText(self, -1, "Workspace path:") 
#         self.workspacePathText = wx.TextCtrl(self, -1, "/docs/new", size=(150, -1));
#         self.workspacePathText.SetHelpText("Workspace Path")
#         self.workspacePathText.SetBackgroundColour("light Gray")
#         self.workspacePathText.SetBackgroundStyle(wx.TE_READONLY)
#         self.workspacePathText.Refresh()
        
#         booShortkNameLabel = wx.StaticText(self, -1, "Short Title:") 
#         bookShortName = ExpandoTextCtrl(self, -1, "", size=(150, -1));

#         authorsLabel = wx.StaticText(self, -1, "Authors:") 
#         authorName = wx.TextCtrl(self, -1, "", size=(50, -1));
#         
#         numberOfPagesLabel = wx.StaticText(self, -1, "Number of pages:") 
#         numberOfPages = wx.TextCtrl(self, -1, "", size=(70, -1));
#         
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.systemTray, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox1.Add(self.workspacePathText, 0, wx.EXPAND|wx.ALL)
        
#         hBox2 = wx.BoxSizer(wx.HORIZONTAL)
#         hBox2.Add(authorsLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox2.Add(authorName, 0, wx.EXPAND|wx.ALL)
        
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3.Add(self.fieldsUnderCoverLabel, 0, wx.EXPAND|wx.ALL,4)
        hBox3.Add(self.lb , 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        
#         hBox4 = wx.BoxSizer(wx.HORIZONTAL)
#         hBox4.Add(numberOfPagesLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox4.Add(numberOfPages, 0, wx.EXPAND|wx.ALL)
        
        vBox.Add(hBox1, 0, wx.EXPAND|wx.ALL, 1)
#         vBox.Add(hBox2, 1, wx.EXPAND|wx.ALL, 1)
        vBox.Add(hBox3, 0, wx.EXPAND|wx.ALL, 1)
#         vBox.Add(hBox4, 1, wx.EXPAND|wx.ALL, 1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox)
        self.SetSizer(sizer)
        

    def EvtListBox(self, event):
        print ('EvtListBox: %s\n' % event.GetString())

    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        label = self.lb.GetString(index)
        status = 'un'
        if self.lb.IsChecked(index):
            status = ''
        print ('Box %s is %schecked \n' % (label, status))
        self.lb.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
 

if __name__ == "__main__":
#     books = FindingBook().findAllBooks()
#     book = None
#     for b in books:
#         book = b
#         break
#     print book
    app = Window()
    app.MainLoop()
