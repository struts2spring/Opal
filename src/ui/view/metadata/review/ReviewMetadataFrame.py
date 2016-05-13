'''
Created on 08-May-2016

@author: vijay
'''
import wx



class ReviewMetadataPanel(wx.Panel):
    '''
    This class review metadata.
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.mainPanel = wx.Panel(self, -1)
        self.mainBox = wx.StaticBox(self.mainPanel, -1, "main box")
        self.left_staticbox = wx.StaticBox(self.mainPanel, -1, "left box")
        self.right_staticbox = wx.StaticBox(self.mainPanel, -1, "right box")
        
        self.helptext = wx.StaticText(self.mainPanel, -1, "Please review downloaded metadata.")
        
        self.title = wx.StaticText(self.mainPanel, -1, "Title")
        self.bookNameLeft = wx.TextCtrl(self.mainPanel, -1,  value="book name left",size=wx.DefaultSize)
        self.bookNameRight = wx.TextCtrl(self.mainPanel, -1, "book name Right")
        
        bitmap=wx.ArtProvider_GetBitmap(wx.ART_GO_BACK)
#         self.okButton = wx.Button(self.mainPanel, -1, 'ok') 
        self.okButton = wx.BitmapButton(self.mainPanel, -1, bitmap, (10, 10),style = wx.BORDER_DEFAULT)
        self.SetProperties()
        self.doLayout()
        self.BindEvents()
        
    def SetProperties(self):
        self.helptext.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Verdana"))
    def doLayout(self):
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        vBox = wx.BoxSizer(wx.VERTICAL)
        
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        
        leftBox = wx.BoxSizer(wx.VERTICAL)
        hRow = wx.BoxSizer(wx.HORIZONTAL)
        
        hRow.Add(self.title , 1, wx.ALIGN_CENTER_VERTICAL | wx.ADJUST_MINSIZE, 5)
        hRow.Add(self.bookNameLeft, 1, wx.ALL | wx.EXPAND, 0)
        leftBox.Add(hRow, 0, wx.ALL | wx.EXPAND, 0)
        leftStaticBoxSizer = wx.StaticBoxSizer(self.left_staticbox, wx.HORIZONTAL)
        
        leftStaticBoxSizer.Add(leftBox, 0, wx.ALL | wx.EXPAND, 10)  
        
        
        rightBox = wx.BoxSizer(wx.VERTICAL)
        rightBox.Add(self.bookNameRight)
        rightStaticBoxSizer = wx.StaticBoxSizer(self.right_staticbox, wx.HORIZONTAL)
        rightStaticBoxSizer.Add(rightBox, 0, wx.ALL | wx.EXPAND, 10)  
        
        centerBox = wx.BoxSizer(wx.VERTICAL)
        centerBox.Add(wx.StaticText(self, -1, label = " "), 1,wx.EXPAND | wx.ALL,5) 
        centerBox.Add(self.okButton)
        
        hBox.Add(leftStaticBoxSizer, 1, wx.EXPAND | wx.ALL, 0)
        hBox.Add(centerBox)
        hBox.Add(rightStaticBoxSizer, 1, wx.EXPAND | wx.ALL, 0)
        
#         vBox.Add(hBox, 0, wx.ALL | wx.EXPAND, 0) 
        vBoxSizer = wx.StaticBoxSizer(self.mainBox, wx.VERTICAL) 
#         hBox.Add(topleft, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        
        vBox.Add(self.helptext, 0, wx.ALL | wx.ADJUST_MINSIZE, 2)
        vBoxSizer.Add(hBox, 0, wx.ALL | wx.EXPAND, 0) 
        
        vBox.Add(vBoxSizer, 0, wx.ALL | wx.EXPAND, 0) 
        self.mainPanel.SetAutoLayout(True)
        self.mainPanel.SetSizer(vBox)
        vBox.Fit(self.mainPanel)
        vBox.SetSizeHints(self.mainPanel)
        mainsizer.Add(self.mainPanel, 1, wx.EXPAND, 0)
        self.SetSizer(mainsizer)
        mainsizer.Layout()  
    
#----------------------------------------------------------------------
    def BindEvents(self):
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
    def onClose(self, event):
        self.Destroy()
class ReviewFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title='Review metadata', size=(600, 400))
        self.panel = ReviewMetadataPanel(self)          
        self.Show()
if __name__ == '__main__':
    app = wx.App(0)
    frame = ReviewFrame(None)
    app.MainLoop()  


# VBox
#     vBoxSizer
#         hBox
#             StaticBox
#             StaticBox
        
