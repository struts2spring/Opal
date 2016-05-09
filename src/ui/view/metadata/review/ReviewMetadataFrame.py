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
        self.mainpanel = wx.Panel(self, -1)
        self.sizer_5_staticbox = wx.StaticBox(self.mainpanel, -1, "Example 2")
        self.sizer_4_staticbox = wx.StaticBox(self.mainpanel, -1, "Example 1")
        
    
    def doLayout(self):

        pass
#----------------------------------------------------------------------
class ReviewFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title='Review metadata', size=(600, 400))
        self.panel = ReviewMetadataPanel(self)
        self.Show()
if __name__ == '__main__':
    app = wx.App(0)
    frame = ReviewFrame(None)
    app.MainLoop()  
