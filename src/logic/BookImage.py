import os
import subprocess


class BookImage():

    def __init__(self):
        pass

    def getBookImage(self, filePath=None, name=None):

        '''
        convert -thumbnail x300 -background white -alpha remove input_file.pdf[0] output_thumbnail.png
        '''
        os.chdir(filePath)
        cmd = 'convert -thumbnail x300 -background white -alpha remove "' + name + '.pdf[0]" "' + name + '.jpg"'
        print cmd
        print subprocess.call(cmd, shell=True)
        print 'getBookImage completed'


if __name__ == "__main__":
    filePath = '/docs/new/3'

    name = 'ST-52900095-16911'
    print 'started'
#     pdfFilePath=os.path.join(filePath, name+'.pdf')
#     imageFilePath=os.path.join(filePath, name+'.jpg')
    BookImage().getBookImage(filePath, name)
    print 'e'
    pass
