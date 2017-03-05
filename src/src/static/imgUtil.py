import wx
import os



class ImageUtil():
    
    def __init__(self):
        self.icons = {}
        path = os.path.abspath(os.path.join(os.path.dirname(__file__) , ".." ,  "images"))
        ls = os.listdir(path)
        for l in ls:
            x = l.split('.')[0:1][0]
            self.icons[x] = os.path.join(path,l)
        pass
    
    def getBitmap(self, iconName=None, size=None):
        image = wx.ImageFromBitmap(wx.Bitmap(self.icons.get(iconName)))
        if size:
            width, height=size
            image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result


    def commandLine(self):
        '''
        convert -quality 100 -resize 32x34 "cbr.png" "cbr.png"
        '''
        pass
        

if __name__ == "__main__":
    x = ImageUtil()
    
    print x.getBitmap(iconName='pdf')
    
#     x._choices.get('pdf')
        
