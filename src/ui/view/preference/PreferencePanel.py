import wx

class PreferencePanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        
        self.st = wx.StaticLine(self, wx.ID_ANY)
        # Make and layout the controls
        fs = self.GetFont().GetPointSize()
        bf = wx.Font(fs+4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs+2, wx.SWISS, wx.NORMAL, wx.NORMAL)

        self.header = wx.StaticText(self, -1, "Opal Preference")
        self.header.SetFont(bf)
        vBox.Add(self.header, 0, wx.ALL | wx.EXPAND, 5)
        vBox.Add(self.st, 0, wx.ALL | wx.EXPAND, 5)
        
        bookNameLabel = wx.StaticText(self, -1, "Title:") 
        bookName = wx.TextCtrl(self, -1, "", size=(150, -1));
        
#         booShortkNameLabel = wx.StaticText(self, -1, "Short Title:") 
#         bookShortName = ExpandoTextCtrl(self, -1, "", size=(150, -1));

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

#         hBox3.Add(booShortkNameLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox3.Add(bookShortName, 0, wx.EXPAND|wx.ALL)
        
        hBox4 = wx.BoxSizer(wx.HORIZONTAL)
        hBox4.Add(numberOfPagesLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox4.Add(numberOfPages, 0, wx.EXPAND|wx.ALL)
        
        vBox.Add(hBox1, 0, wx.EXPAND|wx.ALL, 1)
        vBox.Add(hBox2, 0, wx.EXPAND|wx.ALL, 1)
        vBox.Add(hBox3, 0, wx.EXPAND|wx.ALL, 1)
        vBox.Add(hBox4, 0, wx.EXPAND|wx.ALL, 1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox)
        self.SetSizer(sizer)

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = PreferencePanel(frame)
    frame.Show()
    app.MainLoop()