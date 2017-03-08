import wx
import wx.aui
# import images # contains toolbar icons

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                            "AUI Tutorial",
                            size=(600,400))

        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        notebook = wx.aui.AuiNotebook(self)
        nb_panel = TabPanel(notebook)
        my_panel = MyPanel(self)
        notebook.AddPage(nb_panel, "First Tab", False)

        self._mgr.AddPane(notebook,
                          wx.aui.AuiPaneInfo().Name("notebook-content").
                          CenterPane().PaneBorder(False))
        self._mgr.AddPane(my_panel,
                          wx.aui.AuiPaneInfo().Name("txtctrl-content").
                          CenterPane().PaneBorder(False))
        self._mgr.GetPane("notebook-content").Show().Top().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("txtctrl-content").Show().Bottom().Layer(1).Row(0).Position(0)

        self._mgr.Update()


class MyPanel(wx.Panel):
    """
    My panel with a toolbar and richtextctrl
    """
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent,id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)

        toolbar = wx.ToolBar(self,-1)
        toolbar.AddLabelTool(wx.ID_EXIT, '',wx.art_q)
        self.Bind(wx.EVT_TOOL, self.OnExit, id=wx.ID_EXIT)

        toolbar.Realize()
        sizer.Add(toolbar,proportion=0,flag=wx.ALL | wx.ALIGN_TOP)

        text = ""
        txtctrl = wx.TextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_READONLY|wx.HSCROLL)

        sizer.Add(txtctrl,proportion=0,flag=wx.EXPAND)
        self.SetSizer(sizer)

    def OnExit(self,event):
        self.Close()


class TabPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent,id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)
        sizer.Add(txtTwo, 0, wx.ALL, 5)
        self.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()