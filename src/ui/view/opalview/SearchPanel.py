
import wx
import wx.lib.agw.genericmessagedialog as GMD
from src.logic.search_book import FindingBook
import os
import logging

logger = logging.getLogger('extensive')
try:
	from kivy.logger import Logger
	from src.ui.view.kivy.main import PicturesApp, Picture
except Exception as e:
    logger.error(e, exc_info=True)
from random import randint

# from seleniumx.calling_db import DAO


global searchBooks

class SearchPanel(wx.Panel):
    """
    This will be the first notebook tab
    """
    #----------------------------------------------------------------------
    def __init__(self, parent, *args, **kwargs):
        """"""
#         super(TabPanel, self).__init__(parent=parent,*args, **kwargs)
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.choices = []
        self.vertical = wx.BoxSizer(wx.VERTICAL)
#         txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        searchCaption = wx.StaticText(self, wx.ID_ANY, str('Search name to open (?= any character, * = any string)'))
#         matchingItem = wx.StaticText(self, wx.ID_ANY, str('Matching names:'))
        self.searchCtrl = wx.SearchCtrl(self , id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TE_PROCESS_ENTER)
        self.searchCtrl.SetToolTip(wx.ToolTip('Search Title (book name) or Author'))
        self.searchCtrl.SetDescriptiveText('Search Title (book name) or Author')
        self.searchCtrl.ShowCancelButton(True)
        self.searchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnTextEntered)


#         self.listbox = wx.ListBox(self, choices=self.choices, name='listBox1', size=wx.DefaultSize, pos=wx.Point(8, 48), style=wx.LC_REPORT)
#         self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.doubleclick)
#         self.listbox.Bind(wx.EVT_LISTBOX, self.onSelection)
        self.horizental = wx.BoxSizer()

        search_btn = wx.Button(self, wx.ID_ANY, 'Search')
        self.cb = wx.CheckBox(self, -1, 'Search name to find similar book', (10, 10))
        self.cb.SetValue(True)
        self.Bind(wx.EVT_BUTTON, self.searchBtn, search_btn)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel, self.searchCtrl)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.searchCtrl)
        wx.EVT_CHECKBOX(self, self.cb.GetId(), self.checkboxDefaultClicked)
#         cancel_btn = wx.Button(self, wx.ID_ANY, 'Cancel')
#         self.Bind(wx.EVT_BUTTON, self.cancelBtn, cancel_btn)

#         open_btn = wx.Button(label=u'Open', name='open_btn', parent=self, pos=wx.Point(104, 312), size=wx.Size(87, 28), style=0)
#         cancel_btn = wx.Button( label=u'Cancel', name='cancel_btn', parent=self, pos=wx.Point(104, 312), size=wx.Size(87, 28), style=0)
#         btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
#         self.dialog.Destroy()
#         txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")
#         dirTreeFrame=DirTreeFrame(False)

        self.vertical.Add(searchCaption, 0, wx.EXPAND | wx.ALL, 5)
        self.vertical.Add(self.cb, 0, wx.EXPAND | wx.ALL, 5)
        self.horizental.Add(self.searchCtrl,proportion=3, flag=wx.CENTER)
        self.horizental.Add(search_btn, flag=wx.EXPAND)
#         sizer.Add(matchingItem, 0, wx.EXPAND | wx.ALL, 1)
#         sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)
        self.vertical.Add(self.horizental, proportion=1, flag=wx.EXPAND)
#         tree = DirTree(self)
#         tree=DirTreeFrame(self,False)

#         sizer.Add(tree, 1, wx.EXPAND | wx.ALL)
#         sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizerAndFit(self.vertical)

        self.SetSizer(self.vertical)
    
    def checkboxDefaultClicked(self, event):
        print 'checkboxDefaultClicked',self.cb.GetValue()
            
    def OnTextEntered(self, event):
#         keyCode= event.GetRawKeyCode()
#         print keyCode
        text = self.searchCtrl.GetValue()
        if text != None and text.strip() !='':
            self.doSearch(text.strip())

    def doSearch(self, text):
        global searchedBooks
        name = text
#         print 'doSearch', text
        findingBook=FindingBook()
        totalBookCount=findingBook.countAllBooks()
        books=findingBook.searchingBook(text, self.cb.GetValue())
        searchedBooks=books
        print 'doSearch', text,len(searchedBooks)
        self.GetParent().books=books
        self.GetParent().CreateThumbCtrl()
        grid=self.GetParent().grid

        data = []
        noOfBooks=len(searchedBooks)
        bookId_rowNo_dict={}
        for i in range(noOfBooks):
            d = {}
            data.append((str(i), self.GetParent().books[i].__dict__))
            bookId_rowNo_dict[self.GetParent().books[i].id]=i

        grid._table.data=data
        self.GetParent().grid.bookId_rowNo_dict=bookId_rowNo_dict
        try:
            self.GetParent().picture.root.clear_widgets()
        except Exception as e:
            print e
#         for child in self.GetParent().picture.root..clear_widgets()vchildren:
#             if type(child) == type(Picture):
#                 self.GetParent().picture.root.children.remove(child)
#         self.GetParent().picture.books=books
#         try:
#             self.GetParent().picture.root.clear_widgets(children=None)
#             for book in self.books:
#                 filename=os.path.join(book.bookPath, book.bookImgName)
#     #         for filename in glob(join(curdir, 'images', '*')):
#                 try:
#                     # load the image
#                     picture = PicturesApp(source=filename, rotation=randint(-30, 30))
#                     # add to the main field
#                     self.GetParent().picture.root.add_widget(picture)
#                 except Exception as e:
#                     Logger.exception('Pictures: Unable to load <%s>' % filename)
#         except Exception as e:
#             print e
            
        grid.Reset()
#         grid.books=searchedBooks
#         grid.loadBooks()
        self.GetParent().statusbar.SetStatusText("Filtered : 1 - 50 of "+str(len(books))+ ". Total Books : "+ str(totalBookCount), 1)

#         self.listbox.Clear()
#         employees = DAO().findByName(name)
#         i=0
#         self.rowDict={}
#         for emp in employees:
# #             self.listbox.Append(str(i),str(emp.first_name + ' ' + emp.familay_name))
#             self.listbox.Insert(str(emp.first_name + ' ' + emp.familay_name), i, emp)
#             self.rowDict[i]=emp
#             i=i+1
#         if self.listbox.GetCount() !=0:
#             self.listbox.SetSelection(0)
    def OnSearch(self, evt):
        print "OnSearch"
    def OnCancel(self, evt):
        print "OnCancel"
        text= self.searchCtrl.GetValue()
        self.doSearch(text)
#         self.TopLevelParent.LayoutAll()
#         searchCtrlBook = self.TopLevelParent.FindWindowByName('searchCtrl')
        
    def onSelection(self, event):
        selectedItem=event.GetClientData()
#         tree.Expand(root)
        treeNodeBook=self.TopLevelParent.FindWindowByName('TreeNode')



        print 'onSelection---->',selectedItem
        detailNoteBook = self.TopLevelParent.FindWindowByName('personDetail')

        aui_tabs=None
        if detailNoteBook:
            aui_tabs=detailNoteBook._tabs
            active_page=aui_tabs.GetActivePage()
        personalDetailPanel=aui_tabs._pages[active_page].window
#             pages1=detailNoteBook._tabs._pages
#             personalDetailPanel=detailNoteBook._tabs._pages[len(pages1)-1].window
        if personalDetailPanel:
            personalDetailPanel.removeImage()
        if selectedItem:
            active_page=aui_tabs.GetActivePage()
            page=aui_tabs._pages[active_page]
            aui_tabs._pages[active_page].name=selectedItem.name
            personalDetailPanel.name=selectedItem.name
            personalDetailPanel.layoutSizer(selectedItem)
            personalDetailPanel.Layout()

        personalDetailPan = detailNoteBook.GetChildren()[1]
#         selectedItem=self.rowDict[currentItemIndex]
        print selectedItem
        pass
    def doubleclick(self, event):
        selectedItem=event.GetClientData()

        print 'i---->',selectedItem
#         selectedItem=self.rowDict[currentItemIndex]
        print selectedItem
        pass

    def searchBtn(self, event):
        print 'searchBtn'
        pass
    def cancelBtn(self, event):
        self.Parent.Destroy()

class MyMiniFrame(wx.MiniFrame):
    def __init__(self):
        wx.MiniFrame.__init__(self, None, -1, 'Mini Frame', size=(500, 400))
#         panel = wx.Panel(self, -1, size=(300, 100))
        panel = SearchPanel(self)
#         button = wx.Button(panel, -1, "Close Me", pos=(15, 15))
#         self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
#         self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


# class DemoFrame(wx.Frame):
#     def __init__(self, *args, **kwargs):
#         super(DemoFrame, self).__init__(*args, **kwargs)
# #         wx.Frame.__init__(self, None, wx.ID_ANY, "Panel Tutorial")
#         panel = ResourcePanel(self)
# #         panel.Show()
#
#         self.Show()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyMiniFrame()
    frame.Show()
    app.MainLoop()
