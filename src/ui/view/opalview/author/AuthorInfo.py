import wx
import os






class AuthorPhotoPanel(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.bitmap = None        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize, self)
        
    def OnPaint(self, evt):
        if self.bitmap != None:
            dc = wx.BufferedPaintDC(self)
            dc.Clear()
            dc.DrawBitmap(self.bitmap, 0, 0)
        else:
            pass
    def OnSize(self, event):
        try:
            self.changeBitmapWorker()
        except Exception as e:
            print e
        print 'onsize'
    def changeBitmapWorker(self):
#         relevant_path = "/docs/LiClipse Workspace/img/wallpaper"
#         imgFileName=self.getImgFileName(relevant_path)
#         imgFilePath=os.path.join(relevant_path,imgFileName[0] )
#         imgFilePath = os.path.join(self.currentBook.bookPath, self.currentBook.bookImgName)
        imgFilePath="/docs/commit_opal/Opal/src/ui/view/opalview/author/author.jpg"
#         img2 =  imgFilePath=os.path.join(relevant_path,imgFileName[1] )
        print '---------->', self.GetSize()
        NewW, NewH = self.GetSize()
        if  NewW > 0 and NewH > 0:
            img = wx.Image(imgFilePath, wx.BITMAP_TYPE_ANY)
            img = img.Scale(NewW, NewH)
            self.bitmap = wx.BitmapFromImage(img)
            
    def OnCopyToClipboard(self, event):
        print 'OnCopyToClipboard'

        d = wx.BitmapDataObject(self.bitmap)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(d)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
            print("Image copied to cliboard.\n")
        else:
            print("Couldn't open clipboard!\n")  
            
class AuthorInfoPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.panel = wx.Panel(self, wx.ID_ANY)
        
        topsizer = wx.BoxSizer(wx.VERTICAL)
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        
        ############
        self.photoPanel = AuthorPhotoPanel(self)
        ############
        hBox.Add(vBox, 3, wx.EXPAND, 5)
        hBox.Add(self.photoPanel, 2, wx.EXPAND, 1)
        topsizer.Add(hBox, 3, wx.EXPAND)

        self.panel.SetSizer(topsizer)
        topsizer.SetSizeHints(self.panel)        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel, 1, wx.EXPAND)
#         self.rt = RichTextPanel(self)
        self.sizer.Fit(self)
        self.SetSizer(self.sizer)

class AuthorInfoFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title='Edit Book Metadata', size=(1100, 650))
        self.panel = AuthorInfoPanel(self)
        self.Show()

if __name__ == '__main__':
    app = wx.App(0)
    frame = AuthorInfoFrame(None)
    app.MainLoop() 