'''
Created on 12-Dec-2015

@author: vijay
'''

from yattag import Doc
from bs4 import BeautifulSoup
from src.logic.search_book import FindingBook
import os
import wx.html
from PIL import Image
from src.static.constant import Workspace
import math

class GenerateBookInfo():

    def getHtmlContent(self, book=None):
        '''
        This function is going to provide book info html.
        '''
#         os.chdir(book.bookPath)
        path = os.path.join(Workspace().appPath, "images")
#         path='/home/vijay/Documents/Aptana_Workspace/util/src/ui/view/opalview/images'
        listOfIcons = os.listdir(path)
        iconDict = {}
        for l in listOfIcons:
            name = l.split('.')[0]
            iconDict[name] = os.path.join(path, l)


            lst = os.listdir(book.bookPath)
        name = None
        for l in lst:
            if l.endswith('.jpg') or l.endswith('jpeg'):
                name = l
                break
        print book.bookPath, name
        filepath=os.path.join(path, 'noCover.png')
        print 'GenerateBookInfo.getHtmlContent--->',filepath
        if name!=None and book.bookName!=None: 
            filepath = os.path.join(book.bookPath, name)
            im = Image.open(filepath)
            print im.size
#         book.bookFormat.split(',')
#         iconPath = iconDict[book.bookFormat.lower()]
#         ima= im.resize((200, 250), Image.ANTIALIAS)
#                 print name

        lightGray='#ececec'#'#D3D3D3'
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('style'):
                text('''
                    p.small {
                        font-style: normal;
                        font-size:50%;

                    }
                    ''')
            with tag('head'):
                with tag('title'):
                    text('book info')

            with tag('body'):
                    with tag('h1'):
                        text(book.bookName)

                    if book.subTitle:
                        with tag('h3'):
                            text(book.subTitle)

                    with tag('table', width="100%"):

                        with tag('tr'):
                            with tag('td'):
                                with tag('p'):
                                    img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
                                    originalWidth,originalHeight=img.GetSize()
                                    w,h=300,250
                                    if originalWidth<w :
                                        print 'increase',str(1+(w-originalWidth)/(float(originalWidth)))
                                        h=originalHeight * (1+(w-originalWidth)/(float(originalWidth)))
                                    else:
                                        h=(originalHeight/float(originalWidth))*w
                                        print originalWidth,originalHeight,'decrease',w,int(math.ceil(h))
                                    print '----------- width,height---------->', w,h
                                    doc.stag('img', src=filepath, width=int(w) , height=int(math.ceil(h)), border="1")
#                                     doc.stag('img', src=filepath, width='200' , height='259', border="1")
                            with tag('td'):
                                with tag('h4'):
                                    text('Book Description')
                                with tag('p'):
                                    if book.bookDescription!=None:
                                        text(book.bookDescription)
                    with tag('table', width="100%"):
                        with tag('tr','BGCOLOR="'+lightGray+'"'):
                            with tag('td'):
                                with tag('p', align="right"):
                                    text('Publisher:')
                            with tag('td'):
                                with tag('p'):
                                    if book.publisher!=None:
                                        text(book.publisher)


                        with tag('tr'):
                            with tag('td'):
                                with tag('p', align="right"):
                                    text('by (Authors):')
                            with tag('td'):
                                with tag('p'):
                                    authors = book.authors
                                    authorNameList = list()
                                    for a in authors:
                                        authorNameList.append( a.authorName)
                                    text(','.join(authorNameList))

                        if book.isbn_13:
                            with tag('tr','BGCOLOR="'+lightGray+'"'):
                                with tag('td'):
                                    with tag('p', align="right"):
                                        text('ISBN 13:')
                                with tag('td'):
                                    with tag('p'):
                                        text(book.isbn_13)

#                         with tag('tr'):
#                             with tag('td'):
#                                 with tag('p',align="right"):
#                                     text('Year')
#                             with tag('td'):
#                                 with tag('p'):
#                                     text(book.publishedOn)

                        with tag('tr'):
                            with tag('td'):
                                with tag('p', align="right"):
                                    text('Pages:')
                            with tag('td'):
                                with tag('p'):
                                    if book.numberOfPages:
                                        text(book.numberOfPages)

                        with tag('tr','BGCOLOR="'+lightGray+'"'):
                            with tag('td'):
                                with tag('p', align="right"):
                                    text('Languages:')
                            with tag('td'):
                                with tag('p'):
                                    if book.inLanguage!=None:
                                        text(book.inLanguage)

                        with tag('tr'):
                            with tag('td'):
                                with tag('p', align="right"):
                                    text('File Format:')
                            with tag('td'):
                                with tag('p'):
#                                     text(book.bookFormat)
                                    bookFormatList=book.bookFormat.split(',')
                                    for bookFormat in bookFormatList:
                                        imagePath = os.path.join(Workspace().appPath, "images",(str(bookFormat).lower()).strip()+'.png')
                                        print imagePath
                                        doc.stag('img', src=imagePath, border="0")



                        if book.fileSize:
                            with tag('tr','BGCOLOR="'+lightGray+'"', 'class="small"'):
                                with tag('td'):
                                    with tag('p', align="right"):
                                        text('File Size:')
                                with tag('td'):
                                    with tag('p'):
                                        text(book.fileSize)
#                     with tag('div',  float="left"):
#                         doc.stag('img', src=filepath, width='200' , height='250', border="1")
#                         text(book.bookDescription)
#                         doc.stag('img', src=iconPath, width='42' , height='42', border="1")
#
#                     with tag('div', float="right" ):
#                         doc.stag('img', src=iconPath, width='42' , height='42', border="1")

        content = doc.getvalue()
#         print content
        return content



if __name__ == '__main__':

#     books=FindingBook().searchingBook('webb')
    books = FindingBook().findAllBooks()
    try:
        htmlContent = GenerateBookInfo().getHtmlContent(books[0])
        soup = BeautifulSoup(htmlContent, "lxml")
#         print soup.prettify()
    except:
        pass
    # Open a file in witre mode
    app = wx.PySimpleApp()
    # create a window/frame, no parent, -1 is default ID, title, size
    frame = wx.Frame(None, -1, "HtmlWindow()", size=(610, 380))
    # call the derived class, -1 is default ID

    html1 = wx.html.HtmlWindow(frame, -1, pos=(0, 30), size=(602, 310))
    html1.SetPage(htmlContent)
#     html1.bind(wx.EVT_RIGHT_DOWN, id=wx.NewId(), rightClick)
#     html1.Bind(event, handler, source, id, id2)

#     os.chdir(os.path.dirname(__file__))
#     f = open("info2.html", "r")  # opens file with name of "test.txt"
#     lines = f.readlines()
#     s = ''
#     for l in lines:
#         s = s + str(l)
# 
#     print s

#     html1.SetPage(s)
    # show the frame
    frame.Show(True)
    # start the event loop
    app.MainLoop()


    os.chdir(os.path.dirname(__file__))
    f = open("bookInfo.html", "w")  # opens file with name of "test.txt"
    f.write(soup.prettify())
    f.close()

    pass

# <a target="_blank" href="klematis_big.htm">
#     <img src="/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/1/a_peek_at_computer_electronics.jpg"
#     alt="Professional Java for Web Applications"
#     title="Professional Java for Web Applications" width="200" ></a>
