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
from src.static.constant import Workspace
import os
import random
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

        image = wx.Image(os.path.join(Workspace().appPath, "images", "Library-icon.png"), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(image)
        # set frame icon
        self.SetIcon(icon)


        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Opal version 0.1", 0)
#         self.statusbar.SetStatusText("Opal Version 1.0", 1)

        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))



        # add a bunch of panes


        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().
                          Name("test8").Caption("Tree Pane 1").
                          Left().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))


        self._mgr.AddPane(self.CreateTextCtrl(), wx.aui.AuiPaneInfo().
                          Name("test10").Caption("Text Pane").
                          Bottom().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))



        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().Name("tree_content").
                          CenterPane().Hide())


        self._mgr.AddPane(self.CreateHTMLCtrl(), wx.aui.AuiPaneInfo().Name("html_content").
                          CenterPane())



        # make some default perspectives

        self._mgr.GetPane("tbvert").Hide()

        perspective_all = self._mgr.SavePerspective()

        self._mgr.GetPane("test8").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("test10").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("html_content").Show()


        self._mgr.GetPane("tbvert").Hide()
        self._mgr.GetPane("grid_content").Hide()

        # "commit" all changes made to FrameManager
        self._mgr.Update()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Show How To Use The Closing Panes Event

        self.Bind(wx.EVT_MENU, self.OnCreateTree, id=ID_CreateTree)
        self.Bind(wx.EVT_MENU, self.OnCreateText, id=ID_CreateText)
        self.Bind(wx.EVT_MENU, self.OnCreateHTML, id=ID_CreateHTML)
        self.Bind(wx.EVT_MENU, self.OnCreatePerspective, id=ID_CreatePerspective)
        self.Bind(wx.EVT_MENU, self.OnCopyPerspective, id=ID_CopyPerspective)



        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_About)



        self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective,
                  id2=ID_FirstPerspective + 1000)

        self.Show()



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



    def OnChangeContentPane(self, event):

        self._mgr.GetPane("html_content").Show(event.GetId() == ID_HTMLContent)
        self._mgr.Update()


    def CreateTextCtrl(self):

        text = ("This is text box %d") % (self.n + 1)

        return wx.TextCtrl(self, -1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)



    def CreateTreeCtrl(self):

#         tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
#                            wx.TR_DEFAULT_STYLE | wx.NO_BORDER)

        tree = LazyTree(self)
#         root = tree.AddRoot("General")
#         items = []
# 
#         imglist = wx.ImageList(16, 16, True, 2)
#         imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
#         imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
#         tree.AssignImageList(imglist)
# 
#         items.append(tree.AppendItem(root, "Interface", 0))
#         items.append(tree.AppendItem(root, "Item 2", 0))
#         items.append(tree.AppendItem(root, "Item 3", 0))
#         items.append(tree.AppendItem(root, "Item 4", 0))
#         items.append(tree.AppendItem(root, "Item 5", 0))
# 
#         for ii in xrange(len(items)):
# 
#             id = items[ii]
#             tree.AppendItem(id, "Main interface", 1)
#             tree.AppendItem(id, "Subitem 2", 1)
#             tree.AppendItem(id, "Subitem 3", 1)
#             tree.AppendItem(id, "Subitem 4", 1)
#             tree.AppendItem(id, "Subitem 5", 1)
# 
#         tree.Expand(root)

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

class LazyTree(wx.TreeCtrl):
    ''' LazyTree is a simple "Lazy Evaluation" tree, that is, it only adds 
        items to the tree view when they are needed.'''

    def __init__(self, *args, **kwargs):
        super(LazyTree, self).__init__(*args, **kwargs)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapseItem)
        self.__collapsing = False
        root = self.AddRoot('root')
        self.SetItemHasChildren(root)

    def OnExpandItem(self, event):
        # Add a random number of children and randomly decide which 
        # children have children of their own.
        nrChildren = random.randint(1, 6)
        for childIndex in range(nrChildren):
            child = self.AppendItem(event.GetItem(), 'child %d'%childIndex)
            self.SetItemHasChildren(child, random.choice([True, False]))

    def OnCollapseItem(self, event):
        # Be prepared, self.CollapseAndReset below may cause
        # another wx.EVT_TREE_ITEM_COLLAPSING event being triggered.
        if self.__collapsing:
            event.Veto()
        else:
            self.__collapsing = True
            item = event.GetItem()
            self.CollapseAndReset(item)
            self.SetItemHasChildren(item)
            self.__collapsing = False
            
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
