'''
Created on 05-Dec-2015

@author: vijay
'''



import cStringIO
import PIL.Image
import base64

image_data='\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'

file_like = cStringIO.StringIO(image_data)

img = PIL.Image.open(file_like)
img.show()
img.save('brick-house-gs.png','png')
class ImageStringConverter():

    def imageToString(self, imageFile=None):
        if imageFile:
            with open(imageFile, "rb") as imageFileData:
                str = base64.b64encode(imageFileData.read())
                print str
        return str

    def stringToImage(self, imageData=None):
        if imageData:
            file_like = cStringIO.StringIO(imageData)
            img = PIL.Image.open(file_like)
            img.save('brick-house-gs', 'png')


if __name__ == '__main__':
    pass

