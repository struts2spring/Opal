import wx
import os



class ImageUtil():
    
    def __init__(self):
        self.icons = {}
        path = os.path.join(os.path.dirname(__file__)  , "images")
        includedExtenstions = ['jpeg','jpg', 'bmp', 'png', 'gif']

        fileNames = os.listdir(path)
        for fileName in fileNames:
            fileExtension= fileName.split('.')[-1:][0]
            if fileExtension in includedExtenstions:
                fileNamesWithoutExtension = fileName.split('.')[0:1][0]
                self.icons[fileNamesWithoutExtension] = os.path.join(path,fileName)
        pass
    
    def getBitmap(self, iconName=None, size=None):
        image = wx.ImageFromBitmap(wx.Bitmap(self.icons.get(iconName)))
        if size:
            width, height=size
            image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

if __name__ == "__main__":
    x = ImageUtil()
    
    print x.getBitmap(iconName='zoom')
    
#     x._choices.get('pdf')
        
