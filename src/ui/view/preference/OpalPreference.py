'''
Created on 14-Nov-2015

@author: vijay
'''
import wx
import wx.grid
import wx.html
import wx.aui


import cStringIO
from src.ui.view.SettingPanel import SettingsPanel
from src.ui.view.SizeReportCtrl import SizeReportCtrl
# from view.SettingPanel import SettingsPanel
# from view.SizeReportCtrl import SizeReportCtrl

ID_CreateTree = wx.NewId()
ID_CreateGrid = wx.NewId()
ID_CreateText = wx.NewId()
ID_CreateHTML = wx.NewId()
ID_CreateSizeReport = wx.NewId()
ID_GridContent = wx.NewId()
ID_TextContent = wx.NewId()
ID_TreeContent = wx.NewId()
ID_HTMLContent = wx.NewId()
ID_SizeReportContent = wx.NewId()
ID_CreatePerspective = wx.NewId()
ID_CopyPerspective = wx.NewId()

ID_TransparentHint = wx.NewId()
ID_VenetianBlindsHint = wx.NewId()
ID_RectangleHint = wx.NewId()
ID_NoHint = wx.NewId()
ID_HintFade = wx.NewId()
ID_AllowFloating = wx.NewId()
ID_NoVenetianFade = wx.NewId()
ID_TransparentDrag = wx.NewId()
ID_AllowActivePane = wx.NewId()
ID_NoGradient = wx.NewId()
ID_VerticalGradient = wx.NewId()
ID_HorizontalGradient = wx.NewId()

ID_Settings = wx.NewId()
ID_About = wx.NewId()
ID_FirstPerspective = ID_CreatePerspective + 1000



#----------------------------------------------------------------------
def GetMondrianData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'


def GetMondrianBitmap():
    return wx.BitmapFromImage(GetMondrianImage())


def GetMondrianImage():
    stream = cStringIO.StringIO(GetMondrianData())
    return wx.ImageFromStream(stream)


def GetMondrianIcon():
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon

class OpalPreferenceFrame(wx.Frame):

    def __init__(self, parent):
        title = "Opal Preferences"
        style = wx.DEFAULT_FRAME_STYLE 
        
#         wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        (x,y,maxWidth, maxHeight) = wx.Display().GetGeometry()
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, style=style, size=(maxWidth * .6, maxHeight * .6))
        # tell FrameManager to manage this frame
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self._perspectives = []
        self.n = 0
        self.x = 0

        self.SetIcon(GetMondrianIcon())


        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Opal version 0.1", 0)
#         self.statusbar.SetStatusText("Opal Version 1.0", 1)

        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))



        # add a bunch of panes
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().Name("test1").Caption("Pane Caption").Top().CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test2").Caption("Client Size Reporter").
                          Bottom().Position(1).CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test3").Caption("Client Size Reporter").
                          Bottom().CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test4").Caption("Pane Caption").
                          Left().CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test5").Caption("Pane Caption").
                          Right().CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test6").Caption("Client Size Reporter").
                          Right().Row(1).CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test7").Caption("Client Size Reporter").
                          Left().Layer(1).CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().
                          Name("test8").Caption("Tree Pane 1").
                          Left().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test9").Caption("Min Size 200x100").
                          BestSize(wx.Size(200, 100)).MinSize(wx.Size(200, 100)).
                          Bottom().Layer(1).CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().
                          Name("test10").Caption("Text Pane").
                          Bottom().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Name("test11").Caption("Fixed Pane").
                          Bottom().Layer(1).Position(2).Fixed().CloseButton(False).MaximizeButton(True))

        self._mgr.AddPane(SettingsPanel(self, self), wx.aui.AuiPaneInfo().
                          Name("settings").Caption("Dock Manager Settings").
                          Dockable(True).Float().Hide().CloseButton(True).MaximizeButton(True))

        # create some center panes

#         self._mgr.AddPane(self.CreateGrid(), wx.aui.AuiPaneInfo().Name("grid_content").CenterPane().Hide())
        self._mgr.AddPane(self.CreateGrid(), wx.aui.AuiPaneInfo().Name("grid_content").CenterPane().Show())

        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().Name("tree_content").
                          CenterPane().Hide())

        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().Name("sizereport_content").
                          CenterPane().Hide())

        self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().Name("text_content").
                          CenterPane().Hide())

        self._mgr.AddPane(self.CreateHTMLCtrl(), wx.aui.AuiPaneInfo().Name("html_content").
                          CenterPane())



        # make some default perspectives

        self._mgr.GetPane("tbvert").Hide()

        perspective_all = self._mgr.SavePerspective()

        all_panes = self._mgr.GetAllPanes()

        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()

#         self._mgr.GetPane("tb1").Hide()
#         self._mgr.GetPane("tb5").Hide()
        self._mgr.GetPane("test8").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("test10").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("html_content").Show()

        perspective_default = self._mgr.SavePerspective()

        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()

        self._mgr.GetPane("tb1").Hide()
        self._mgr.GetPane("tb5").Hide()
        self._mgr.GetPane("tbvert").Show()
        self._mgr.GetPane("grid_content").Show()
        self._mgr.GetPane("test8").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("test10").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("html_content").Show()

        perspective_vert = self._mgr.SavePerspective()

        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)
        self._perspectives.append(perspective_vert)

        self._mgr.GetPane("tbvert").Hide()
        self._mgr.GetPane("grid_content").Hide()

        # "commit" all changes made to FrameManager
        self._mgr.Update()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Show How To Use The Closing Panes Event
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)

        self.Bind(wx.EVT_MENU, self.OnCreateTree, id=ID_CreateTree)
        self.Bind(wx.EVT_MENU, self.OnCreateGrid, id=ID_CreateGrid)
        self.Bind(wx.EVT_MENU, self.OnCreateText, id=ID_CreateText)
        self.Bind(wx.EVT_MENU, self.OnCreateHTML, id=ID_CreateHTML)
        self.Bind(wx.EVT_MENU, self.OnCreateSizeReport, id=ID_CreateSizeReport)
        self.Bind(wx.EVT_MENU, self.OnCreatePerspective, id=ID_CreatePerspective)
        self.Bind(wx.EVT_MENU, self.OnCopyPerspective, id=ID_CopyPerspective)

        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowFloating)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_RectangleHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_HintFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentDrag)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowActivePane)

        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_NoGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_VerticalGradient)
        self.Bind(wx.EVT_MENU, self.OnGradient, id=ID_HorizontalGradient)
        self.Bind(wx.EVT_MENU, self.OnSettings, id=ID_Settings)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_GridContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_TreeContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_TextContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_SizeReportContent)
        self.Bind(wx.EVT_MENU, self.OnChangeContentPane, id=ID_HTMLContent)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)

        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_RectangleHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HintFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowFloating)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentDrag)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowActivePane)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VerticalGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HorizontalGradient)


        self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective,
                  id2=ID_FirstPerspective + 1000)

        self.Show()
    def OnPaneClose(self, event):

        caption = event.GetPane().caption

        if caption in ["Tree Pane", "Dock Manager Settings", "Fixed Pane"]:
            msg = "Are You Sure You Want To Close This Pane?"
            dlg = wx.MessageDialog(self, msg, "AUI Question",
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                event.Veto()
            dlg.Destroy()


    def OnClose(self, event):
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()


    def OnExit(self, event):
        self.Close()

    def OnAbout(self, event):

        msg = "wx.aui Demo\n" + \
              "An advanced window management library for wxWidgets\n" + \
              "(c) Copyright 2005-2006, Kirix Corporation"
        dlg = wx.MessageDialog(self, msg, "About wx.aui Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def GetDockArt(self):

        return self._mgr.GetArtProvider()


    def DoUpdate(self):

        self._mgr.Update()


    def OnEraseBackground(self, event):

        event.Skip()


    def OnSize(self, event):
        
        size = self.GetSize()
        print '11', wx.GetDisplaySize() 
        print wx.Display().GetCurrentMode(),':',wx.Display().GetGeometry()
        print size
        event.Skip()


    def OnSettings(self, event):

        # show the settings pane, and float it
        floating_pane = self._mgr.GetPane("settings").Float().Show()

        if floating_pane.floating_pos == wx.DefaultPosition:
            floating_pane.FloatingPosition(self.GetStartPosition())

        self._mgr.Update()


    def OnGradient(self, event):

        gradient = 0

        if event.GetId() == ID_NoGradient:
            gradient = wx.aui.AUI_GRADIENT_NONE
        elif event.GetId() == ID_VerticalGradient:
            gradient = wx.aui.AUI_GRADIENT_VERTICAL
        elif event.GetId() == ID_HorizontalGradient:
            gradient = wx.aui.AUI_GRADIENT_HORIZONTAL

        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE, gradient)
        self._mgr.Update()


    def OnManagerFlag(self, event):

        flag = 0
        eid = event.GetId()

        if eid in [ ID_TransparentHint, ID_VenetianBlindsHint, ID_RectangleHint, ID_NoHint ]:
            flags = self._mgr.GetFlags()
            flags &= ~wx.aui.AUI_MGR_TRANSPARENT_HINT
            flags &= ~wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
            flags &= ~wx.aui.AUI_MGR_RECTANGLE_HINT
            self._mgr.SetFlags(flags)

        if eid == ID_AllowFloating:
            flag = wx.aui.AUI_MGR_ALLOW_FLOATING
        elif eid == ID_TransparentDrag:
            flag = wx.aui.AUI_MGR_TRANSPARENT_DRAG
        elif eid == ID_HintFade:
            flag = wx.aui.AUI_MGR_HINT_FADE
        elif eid == ID_NoVenetianFade:
            flag = wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        elif eid == ID_AllowActivePane:
            flag = wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE
        elif eid == ID_TransparentHint:
            flag = wx.aui.AUI_MGR_TRANSPARENT_HINT
        elif eid == ID_VenetianBlindsHint:
            flag = wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
        elif eid == ID_RectangleHint:
            flag = wx.aui.AUI_MGR_RECTANGLE_HINT

        self._mgr.SetFlags(self._mgr.GetFlags() ^ flag)


    def OnUpdateUI(self, event):

        flags = self._mgr.GetFlags()
        eid = event.GetId()

        if eid == ID_NoGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_NONE)

        elif eid == ID_VerticalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_VERTICAL)

        elif eid == ID_HorizontalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_HORIZONTAL)

        elif eid == ID_AllowFloating:
            event.Check((flags & wx.aui.AUI_MGR_ALLOW_FLOATING) != 0)

        elif eid == ID_TransparentDrag:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_DRAG) != 0)

        elif eid == ID_TransparentHint:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_HINT) != 0)

        elif eid == ID_VenetianBlindsHint:
            event.Check((flags & wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT) != 0)

        elif eid == ID_RectangleHint:
            event.Check((flags & wx.aui.AUI_MGR_RECTANGLE_HINT) != 0)

        elif eid == ID_NoHint:
            event.Check(((wx.aui.AUI_MGR_TRANSPARENT_HINT | 
                          wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT | 
                          wx.aui.AUI_MGR_RECTANGLE_HINT) & flags) == 0)

        elif eid == ID_HintFade:
            event.Check((flags & wx.aui.AUI_MGR_HINT_FADE) != 0);

        elif eid == ID_NoVenetianFade:
            event.Check((flags & wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE) != 0);




    def OnCreatePerspective(self, event):

        dlg = wx.TextEntryDialog(self, "Enter a name for the new perspective:", "AUI Test")

        dlg.SetValue(("Perspective %d") % (len(self._perspectives) + 1))
        if dlg.ShowModal() != wx.ID_OK:
            return

        if len(self._perspectives) == 0:
            self._perspectives_menu.AppendSeparator()

        self._perspectives_menu.Append(ID_FirstPerspective + len(self._perspectives), dlg.GetValue())
        self._perspectives.append(self._mgr.SavePerspective())


    def OnCopyPerspective(self, event):

        s = self._mgr.SavePerspective()

        if wx.TheClipboard.Open():

            wx.TheClipboard.SetData(wx.TextDataObject(s))
            wx.TheClipboard.Close()

    def OnRestorePerspective(self, event):

        self._mgr.LoadPerspective(self._perspectives[event.GetId() - ID_FirstPerspective])


    def GetStartPosition(self):

        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))

        return wx.Point(pt.x + x, pt.y + x)


    def OnCreateTree(self, event):
        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Tree Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(150, 300)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateGrid(self, event):
        self._mgr.AddPane(self.CreateGrid(), wx.aui.AuiPaneInfo().
                          Caption("Grid").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateHTML(self, event):
        self._mgr.AddPane(self.CreateHTMLCtrl(), wx.aui.AuiPaneInfo().
                          Caption("HTML Content").
                          Float().FloatingPosition(self.GetStartPosition()).
                          FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateText(self, event):
        self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Text Control").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnCreateSizeReport(self, event):
        self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().
                          Caption("Client Size Reporter").
                          Float().FloatingPosition(self.GetStartPosition()).
                          CloseButton(True).MaximizeButton(True))
        self._mgr.Update()


    def OnChangeContentPane(self, event):

        self._mgr.GetPane("grid_content").Show(event.GetId() == ID_GridContent)
        self._mgr.GetPane("text_content").Show(event.GetId() == ID_TextContent)
        self._mgr.GetPane("tree_content").Show(event.GetId() == ID_TreeContent)
        self._mgr.GetPane("sizereport_content").Show(event.GetId() == ID_SizeReportContent)
        self._mgr.GetPane("html_content").Show(event.GetId() == ID_HTMLContent)
        self._mgr.Update()


    def CreateTextCtrl(self):

        text = ("This is text box %d") % (self.n + 1)

        return wx.TextCtrl(self, -1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)



    def CreateGrid(self):

        grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250),
                            wx.NO_BORDER | wx.WANTS_CHARS)

        grid.CreateGrid(50, 20)

        return grid


    def CreateTreeCtrl(self):

        tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)

        root = tree.AddRoot("AUI Project")
        items = []

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
        tree.AssignImageList(imglist)

        items.append(tree.AppendItem(root, "Item 1", 0))
        items.append(tree.AppendItem(root, "Item 2", 0))
        items.append(tree.AppendItem(root, "Item 3", 0))
        items.append(tree.AppendItem(root, "Item 4", 0))
        items.append(tree.AppendItem(root, "Item 5", 0))

        for ii in xrange(len(items)):

            id = items[ii]
            tree.AppendItem(id, "Subitem 1", 1)
            tree.AppendItem(id, "Subitem 2", 1)
            tree.AppendItem(id, "Subitem 3", 1)
            tree.AppendItem(id, "Subitem 4", 1)
            tree.AppendItem(id, "Subitem 5", 1)

        tree.Expand(root)

        return tree


    def CreateSizeReportCtrl(self, width=80, height=80):

        ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition,
                              wx.Size(width, height), self._mgr)
        return ctrl


    def CreateHTMLCtrl(self):
        ctrl = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(400, 300))
        if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
            ctrl.SetStandardFonts()
        ctrl.SetPage(self.GetIntroText())
        return ctrl


    def GetIntroText(self):
        return overview

overview = """\
<html><body>
<h3>wx.aui, the Advanced User Interface module</h3>

<br/><b>Overview</b><br/>

<p>wx.aui is an Advanced User Interface library for the wxWidgets toolkit
that allows developers to create high-quality, cross-platform user
interfaces quickly and easily.</p>

<p><b>Features</b></p>

<p>With wx.aui developers can create application frameworks with:</p>

<ul>
<li>Native, dockable floating frames</li>
<li>Perspective saving and loading</li>
<li>Native toolbars incorporating real-time, &quot;spring-loaded&quot; dragging</li>
<li>Customizable floating/docking behavior</li>
<li>Completely customizable look-and-feel</li>
<li>Optional transparent window effects (while dragging or docking)</li>
</ul>

</body></html>
"""

if __name__ == "__main__":
    app = wx.App()
    frame = OpalPreferenceFrame(None)
    frame.Show()
    app.MainLoop()
