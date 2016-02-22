import os
import subprocess
import sys


class BookImage():

    def __init__(self):
        pass

    def getBookImage(self, filePath=None, name=None, bookFormat=None):

        '''
        convert -thumbnail x300 -background white -alpha remove input_file.pdf[0] output_thumbnail.png
        '''
        os.chdir(filePath)
        if 'pdf'==bookFormat:
            cmd = 'convert -thumbnail x300 -background white -alpha remove "' + name + '.pdf[0]" "' + name + '.jpg"'
            print cmd
            print subprocess.call(cmd, shell=True)
        elif 'mobi'==bookFormat:
            print 'work in progress'
        print 'getBookImage completed'


if __name__ == "__main__":
    filePath=None
    if sys.platform=='win32':
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
