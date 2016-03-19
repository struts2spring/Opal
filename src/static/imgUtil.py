import wx
import os



class ImageUtil():
    
    def __init__(self):
        self.icons = {}
        path = os.path.join(os.path.dirname(__file__) , ".." , 'ui' , 'view' , 'opalview' , "images")
        ls = os.listdir(path)
        for l in ls:
            x = l.split('.')[0:1][0]
            self.icons[x] = os.path.join(path,l)
        pass
    
    def getBitmap(self, iconName=None):
        return wx.Bitmap(self.icons.get(iconName))
            
#         self._choices = {
#             'pdf': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep + "pdf.png"),
#             'chm': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep + "chm.png"),
#             'mobi': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep + "mobi.png"),
#             'epub': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep + "epub.png"),
#             'doc': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep + "doc.png")
#             }
        
if __name__ == "__main__":
    x = ImageUtil()
    
    print x.getBitmap(iconName='pdf')
    
#     x._choices.get('pdf')
        
