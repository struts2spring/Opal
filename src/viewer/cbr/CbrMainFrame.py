from wx.lib.agw import aui
import wx.html
from src.audit.singletonLoggerLogging import Logger
from src.viewer.cbr.PhotoFrame import PropertyPhotoPanel
from src.viewer.cbr.ThumbCrtl import ThumbnailCtrl, NativeImageHandler
from src.viewer.cbr.imgUtil import ImageUtil
from src.viewer.cbr.ExtractImage import Extractor
import os

logger = Logger('cbr')


# -- SizeReportCtrl --
# (a utility control that always reports it's client size)

class SizeReportCtrl(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                size=wx.DefaultSize, mgr=None):

        wx.PyControl.__init__(self, parent, id, pos, size, style=wx.NO_BORDER)
        self._mgr = mgr

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        size = self.GetClientSize()

        s = "Size: %d x %d" % (size.x, size.y)

        dc.SetFont(wx.NORMAL_FONT)
        w, height = dc.GetTextExtent(s)
        height += 3
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, size.x, size.y)
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawLine(0, 0, size.x, size.y)
        dc.DrawLine(0, size.y, size.x, 0)
        dc.DrawText(s, (size.x - w) / 2, (size.y - height * 5) / 2)

        if self._mgr:

            pi = self._mgr.GetPane(self)

            s = "Layer: %d" % pi.dock_layer
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 1))

            s = "Dock: %d Row: %d" % (pi.dock_direction, pi.dock_row)
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 2))

            s = "Position: %d" % pi.dock_pos
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 3))

            s = "Proportion: %d" % pi.dock_proportion
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 4))


    def OnEraseBackground(self, event):

        pass


    def OnSize(self, event):

        self.Refresh()










class CbrFrame(wx.Frame):

    def __init__(self, parent, book=None, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER,):
        title = "Opal"
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        self.book = book
        self._mgr = aui.AuiManager()

        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self)

        # set frame icon
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
        self.CreateStatusBar()
        self.GetStatusBar().SetStatusText("Ready")

        self.BuildPanes()
        self.CreateMenuBar()
        self.BindEvents()
        self.Show()
        
    def BuildPanes(self):

        # min size for the frame itself isn't completely done.
        # see the end up AuiManager.Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))
        
        # prepare a few custom overflow elements for the toolbars' overflow buttons

        prepend_items, append_items = [], []
        item = aui.AuiToolBarItem()

        item.SetKind(wx.ITEM_SEPARATOR)
        append_items.append(item)

        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_NORMAL)
#         item.SetId(ID_CustomizeToolbar)
        item.SetLabel("Customize...")
        append_items.append(item)


        # create some toolbars
        ID_SampleItem = wx.ID_ANY
        print '--------->', ID_SampleItem
        tb1 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        tb1.SetToolBitmapSize(wx.Size(48, 48))
        tb1.AddSimpleTool(ID_SampleItem + 2, "Test", wx.ArtProvider.GetBitmap(wx.ART_GO_BACK))
        tb1.AddSimpleTool(ID_SampleItem + 4, "Test", wx.ArtProvider.GetBitmap(wx.ART_GO_HOME))
        tb1.AddSimpleTool(ID_SampleItem + 3, "Test", wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD))
        tb1.AddSimpleTool(ID_SampleItem + 5, "Test", wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.AddSeparator()
        tb1.AddSimpleTool(tool_id=(ID_SampleItem + 1), label="bookmark", short_help_string="Bookmark", bitmap=wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK))
        tb1.SetCustomOverflowItems(prepend_items, append_items)
        tb1.Realize()
        
        tb2 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        tb2.SetToolBitmapSize(wx.Size(16, 16))

#         tb2_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))
        imageUtil = ImageUtil() 
        zoom = imageUtil.getBitmap(iconName='zoom')
        comments = imageUtil.getBitmap(iconName='comments')
        doublePage = imageUtil.getBitmap(iconName='double-page')
        fitbest = imageUtil.getBitmap(iconName='fitbest')
        fitheight = imageUtil.getBitmap(iconName='fitheight')
        gimpRotate180 = imageUtil.getBitmap(iconName='gimp-rotate-180')
        gimpRotate270 = imageUtil.getBitmap(iconName='gimp-rotate-270')
        gimpRotate90 = imageUtil.getBitmap(iconName='gimp-rotate-90')
        lens = imageUtil.getBitmap(iconName='lens')
        fitwidth = imageUtil.getBitmap(iconName='fitwidth')
        
        tb2.AddSimpleTool(ID_SampleItem + 6, "Test", zoom)
        tb2.AddSimpleTool(ID_SampleItem + 7, "Test", comments)
        tb2.AddSimpleTool(ID_SampleItem + 8, "Test", doublePage)
        tb2.AddSimpleTool(ID_SampleItem + 9, "Test", fitbest)
        tb2.AddSeparator()
        tb2.AddSimpleTool(ID_SampleItem + 10, "Test", fitheight)
        tb2.AddSimpleTool(ID_SampleItem + 11, "Test", gimpRotate180)
        tb2.AddSeparator()
        tb2.AddSimpleTool(ID_SampleItem + 12, "Test", lens)
        tb2.AddSimpleTool(ID_SampleItem + 13, "Test", fitwidth)
        tb2.AddSimpleTool(ID_SampleItem + 14, "Test", gimpRotate270)
        tb2.AddSimpleTool(ID_SampleItem + 15, "Test", gimpRotate90)
        tb2.SetCustomOverflowItems(prepend_items, append_items)
        tb2.Realize()
        
        # add the toolbars to the manager
        self._mgr.AddPane(tb1, aui.AuiPaneInfo().Name("tb1").Caption("Big Toolbar"). ToolbarPane().Top())
        self._mgr.AddPane(tb2, aui.AuiPaneInfo().Name("tb2").Caption("Toolbar 2").ToolbarPane().Top().Row(0))
        
        
        # add a bunch of panes
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().Name("test1").Caption("Pane Caption").Top().MinimizeButton(True))        
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
#                           Name("test2").Caption("Client Size Reporter").
#                           Bottom().Position(1).CloseButton(True).MaximizeButton(True).
#                           MinimizeButton(True).CaptionVisible(True, left=True))
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
#                           Name("test3").Caption("Client Size Reporter").
#                           Bottom().CloseButton(True).MaximizeButton(True).MinimizeButton(True).
#                           CaptionVisible(True, left=True))
        self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().Name("test4").Caption("Thumbnails").Left().BestSize(200, 200))                
        self._mgr.AddPane(self.photoCtrl(), aui.AuiPaneInfo().Name("photo").Caption("Current page").Center().CloseButton(False))                
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
#                           Name("test5").Caption("No Close Button").Right().CloseButton(False))
#         
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
#                           Name("test6").Caption("Client Size Reporter").Right().Row(1).
#                           CloseButton(True).MaximizeButton(True).MinimizeButton(True))
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), aui.AuiPaneInfo().
#                           Name("test7").Caption("Client Size Reporter").Left().Layer(1).
#                           CloseButton(True).MaximizeButton(True).MinimizeButton(True))        
#         self._mgr.AddPane(self.CreateTreeCtrl(), aui.AuiPaneInfo().Name("test8").Caption("Tree Pane").
#                           Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True).
#                           MinimizeButton(True))

                        
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
        # "commit" all changes made to AuiManager
        self._mgr.Update()

 
        
       
    def CreateMenuBar(self):

        # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "Exit")
        
        view_menu = wx.Menu()
        
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "About...")

        mb.Append(file_menu, "&File")
        mb.Append(view_menu, "&View")
        mb.Append(help_menu, "&Help")
        self.SetMenuBar(mb)
    def BindEvents(self):
        pass
#         self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
    def CreateSizeReportCtrl(self, width=500, height=80):
        filePath = os.path.join(self.book.bookPath, self.book.bookName+"."+self.book.bookFormat)
        extractor = Extractor(filePath=filePath)
        firstPage=extractor.extractFirstPageCbrImage()
        self.firstPage="/tmp/1/"+firstPage
#         ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition, wx.Size(width, height), self._mgr)
        self.thumbnail = ThumbnailCtrl(self, imagehandler=NativeImageHandler)
        self.thumbnail._scrolled.EnableToolTips(enable=True)
        
#         thumbnail = TC.ThumbnailCtrl(self, imagehandler=TC.NativeImageHandler)

        self.thumbnail.ShowDir("/tmp/1")
        return self.thumbnail
    
    
    
    def photoCtrl(self):
        
        self.photoPanel = PropertyPhotoPanel(self, imagePath=self.firstPage) 
        return self.photoPanel
if __name__ == "__main__":
    
    logger = Logger('cbr')
    logger.info("this testname.")
    app = wx.App()
    frame = CbrFrame(None, book=None)
    frame.Show()
    app.MainLoop()
