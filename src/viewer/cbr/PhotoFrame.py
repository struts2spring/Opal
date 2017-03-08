import wx
import os
from src.logic.search_book import FindingBook
import traceback


class PropertyPhotoPanel(wx.Panel):

    def __init__(self, parent=None, imagePath=None):
        wx.Panel.__init__(self, parent, id=-1)
        self.Bind(wx.EVT_SIZE, self.OnSize, self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.parent = parent
        self.bitmap = None
        self.imagePath = imagePath
        
    def OnRightClick(self, event):
        print("PropertyPhotoPanel.OnRightClick()\n")
        self.createMenu()
        
    def OnContextMenu(self, event):
        print("OnContextMenu\n")

        # only do this part the first time so the events are only bound once
        #
        # Yet another anternate way to do IDs. Some prefer them up top to
        # avoid clutter, some prefer them close to the object of interest
        # for clarity. 
        self.createMenu()
    
    def createMenu(self):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1, "Copy book cover")
#         bmp = images.Smiles.GetBitmap()
#         item.SetBitmap(bmp)
        menu.AppendItem(item)
        # add some other items
        menu.Append(self.popupID2, "Download book cover")
        menu.Append(self.popupID3, "Generate book cover")
        menu.Append(self.popupID4, "Open book")
        
        
        self.Bind(wx.EVT_MENU, self.OnCopyToClipboard, id=self.popupID1)
        self.Bind(wx.EVT_MENU, self.downloadCover, id=self.popupID2)
        self.Bind(wx.EVT_MENU, self.generateCover, id=self.popupID3)
        self.Bind(wx.EVT_MENU, self.openBook, id=self.popupID4)
        
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
        
    def downloadCover(self, event):
        print 'downloadCover'
    def generateCover(self, event):
        print 'generateCover'
    def openBook(self, event):
        print 'openBook'        
        
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
              
    def OnSize(self, event):
        self.changeBitmapWorker()
        print 'onsize'

    def OnPaint(self, evt):
        if self.bitmap != None:
            dc = wx.BufferedPaintDC(self)
            dc.Clear()
            dc.DrawBitmap(self.bitmap, 0, 0)
#             self.imagePath = "whatever"
#             w, h = 100, 100
#             tw, th = dc.GetTextExtent(text)
#             dc.DrawText(text, (w - tw) / 2, (h - th) / 2)
        else:
            pass
    def changeBitmapWorker(self):
#         relevant_path = "/docs/LiClipse Workspace/img/wallpaper"
#         imgFileName=self.getImgFileName(relevant_path)
#         imgFilePath=os.path.join(relevant_path,imgFileName[0] )
        try:
    #         img2 =  imgFilePath=os.path.join(relevant_path,imgFileName[1] )
    #         imgFilePath="cat.bmp"
            if self.imagePath !=None:
                print '---------->', self.GetSize()
                NewW, NewH = self.GetSize()
                newSize = self.GetSize()
                if  NewW > 0 and NewH > 0:
                    img = wx.Image(self.imagePath, wx.BITMAP_TYPE_ANY)
                    originalsize = (img.GetWidth(), img.GetHeight())
                    print '-originalsize--------->', originalsize, originalsize[0] / float(originalsize[1])
                    originalRatio = originalsize[0] / float(originalsize[1])
                    print '-new--------->', min(newSize[0], originalsize[0]), min(newSize[1], originalsize[1])
                    minWidthHeight = min(min(newSize[0], originalsize[0]), min(newSize[1], originalsize[1]))
                    if minWidthHeight == min(newSize[0], originalsize[0]):
                        height = minWidthHeight / originalRatio
                        width = minWidthHeight
                    else:
                        height = minWidthHeight
                        width = minWidthHeight * originalRatio
                        
                    img.Rescale(width,height, wx.IMAGE_QUALITY_NORMAL)
    #                 img = img.Scale(NewW, NewH)
                    self.bitmap = wx.BitmapFromImage(img)
                    self.Refresh()
        except:
            traceback.print_exc()   
class ReviewFrame(wx.Frame):
    def __init__(self, parent, imagePath='/docs/github/Opal/src/viewer/cbr/ext/1/All Star Superman 001-000.jpg'):
        wx.Frame.__init__(self, parent, -1, title='Photo', size=(600, 400))
        self.panel = PropertyPhotoPanel(self, imagePath='/docs/github/Opal/src/viewer/cbr/ext/1/All Star Superman 001-000.jpg')          
        self.Show()            
if __name__ == '__main__':
    books = FindingBook().findAllBooks()
    book = None
    for b in books:
        book = b
        break
    print book
    app = wx.App(0)
    frame = ReviewFrame(None, imagePath='/docs/github/Opal/src/viewer/cbr/ext/1/All Star Superman 001-000.jpg')
    app.MainLoop()  
