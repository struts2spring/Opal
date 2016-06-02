import os
import subprocess
import sys
from src.ui.view.epub.opal_epub_worker import EpubBook

from wand.image import Image

class BookImage():

    def __init__(self):
        pass

    def getPdfBookImage(self, name=None):
        # Converting first page into JPG
#         with Image(filename=sourcePdf) as img:
#             img.save(filename=destImg)
        cmd = 'convert -background white -alpha remove "' + name + '.pdf[0]' + '" "' + name + '.jpg' + '"'
        subprocess.call(cmd, shell=True)
        
    def getDjuvBookImage(self, name=None):
        cmd = 'ddjvu -page=1 -format=pnm "' + name + '.djvu" 1.pnm && pnmtojpeg 1.pnm > "' + name + '.jpg" && rm *.pnm'
        subprocess.call(cmd, shell=True)
        
    def getChmBookImage(self, name=None):
        print 'getChmBookImage'
        
    def getBookImage(self, filePath=None, name=None, bookFormat=None):

        '''
        @name book_file_name
        convert -thumbnail x300 -background white -alpha remove input_file.pdf[0] output_thumbnail.png
        '''
        os.chdir(filePath)
        if 'pdf' == bookFormat:
            self.getPdfBookImage(name)

        elif 'djvu' == bookFormat:
            self.getDjuvBookImage(name)
            
        elif 'chm' == bookFormat:
            self.getChmBookImage(name)
            
        elif 'epub' == bookFormat:
            file_name = name + '.epub'
            epubBook = EpubBook()
            epubBook.open(file_name)
        
            epubBook.parse_contents()
            epubBook.extract_cover_image(name+'.jpg', outdir='.',)
            
        elif 'mobi' == bookFormat:
            print 'work in progress'
        print 'getBookImage completed'


if __name__ == "__main__":
    filePath = None
    if sys.platform == 'win32':
        filePath = 'c://new_1//3'
    else:
        filePath = '/docs/new_1/3'
        

    name = 'Java Test-Driven Development'
    print 'started'
#     pdfFilePath=os.path.join(filePath, name+'.pdf')
#     imageFilePath=os.path.join(filePath, name+'.jpg')
    BookImage().getBookImage(filePath, name)
    print 'e'
    pass
