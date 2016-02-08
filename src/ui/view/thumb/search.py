
import wx
import wx.lib.agw.thumbnailctrl as TC
import os

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


#         image = wx.Image('pdf.png', wx.BITMAP_TYPE_ANY)
#         img=image.Scale(18,18)
#         imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))

        self.search = wx.SearchCtrl(self, size=wx.DefaultSize, style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        self.search.SetMenu(self.MakeMenu())
        
        self.thumbnail = TC.ThumbnailCtrl(self, imagehandler=TC.NativeImageHandler)
#         self.thumbnail.ShowDir("/home/vijay/Documents/LiClipse Workspace/flow/img")

        vbox_1 = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox_1 = wx.BoxSizer(wx.HORIZONTAL)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((15, 15))
#         hbox.Add(imageBitmap, 0, wx.ALL, 17)
        vbox.Add(self.search, 0, wx.EXPAND, 15)
#         vbox.Add(self.thumbnail, 1, wx.EXPAND | wx.ALL, 10)
        hbox.Add(vbox, 9,wx.EXPAND|wx.RIGHT, 0)
        
        vbox_1.Add(hbox, 1,wx.EXPAND|wx.RIGHT, 0)
        hbox_1.Add(self.thumbnail, 1, wx.EXPAND | wx.ALL, 0)
        vbox_1.Add(hbox_1, 9,wx.EXPAND|wx.RIGHT, 0)
        
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
         

#----------------------------------------------------------------------
class SearchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title='Test', size=(600, 400))
        self.panel = TestPanel(self)
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