'''
Created on 08-Dec-2015

@author: vijay
'''

import wx
import wx.grid
import wx.html
import wx.lib.gridmovers   as  gridmovers
import wx.grid             as  gridlib
import os
import sys
from src.logic.search_book import FindingBook
import random



#---------------------------------------------------------------------------

class MegaTable(gridlib.PyGridTableBase):
    """
    A custom wx.Grid Table using user supplied data
    """
    def __init__(self, data, colnames, plugins):
        """data is a list of the form
        [(rowname, dictionary),
        dictionary.get(colname, None) returns the data for column
        colname
        """
        # The base class must be initialized *first*
        gridlib.PyGridTableBase.__init__(self)
        self.data = data
        self.colnames = colnames
        self.plugins = plugins or {}
        # XXX
        # we need to store the row length and column length to
        # see if the table has changed size
        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()

    def GetNumberCols(self):
        return len(self.colnames)

    def GetNumberRows(self):
        return len(self.data)

    def GetColLabelValue(self, col):
        return self.colnames[col]

    def GetRowLabelValue(self, row):
        return "row %03d" % int(self.data[row][0])

    def GetValue(self, row, col):
        return str(self.data[row][1].get(self.GetColLabelValue(col), ""))

    def GetRawValue(self, row, col):
        return self.data[row][1].get(self.GetColLabelValue(col), "")

    def SetValue(self, row, col, value):
        self.data[row][1][self.GetColLabelValue(col)] = value

    def ResetView(self, grid):
        """
        (Grid) -> Reset the grid view.   Call this to
        update the grid if rows and columns have been added or deleted
        """
        grid.BeginBatch()

        for current, new, delmsg, addmsg in [
            (self._rows, self.GetNumberRows(), gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED),
            (self._cols, self.GetNumberCols(), gridlib.GRIDTABLE_NOTIFY_COLS_DELETED, gridlib.GRIDTABLE_NOTIFY_COLS_APPENDED),
        ]:

            if new < current:
                msg = gridlib.GridTableMessage(self,delmsg,new,current-new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = gridlib.GridTableMessage(self,addmsg,new-current)
                grid.ProcessTableMessage(msg)
                self.UpdateValues(grid)

        grid.EndBatch()

        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()
        # update the column rendering plugins
        self._updateColAttrs(grid)

        # update the scrollbars and the displayed part of the grid
        grid.AdjustScrollbars()
        grid.ForceRefresh()


    def UpdateValues(self, grid):
        """Update all displayed values"""
        # This sends an event to the grid table to update all of the values
        msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        grid.ProcessTableMessage(msg)

    def _updateColAttrs(self, grid):
        """
        wx.Grid -> update the column attributes to add the
        appropriate renderer given the column name.  (renderers
        are stored in the self.plugins dictionary)

        Otherwise default to the default renderer.
        """
        col = 0

        for colname in self.colnames:
            attr = gridlib.GridCellAttr()
            if colname in self.plugins:
                renderer = self.plugins[colname](self)

                if renderer.colSize:
                    grid.SetColSize(col, renderer.colSize)

                if renderer.rowSize:
                    grid.SetDefaultRowSize(renderer.rowSize)

                attr.SetReadOnly(True)
                attr.SetRenderer(renderer)

            grid.SetColAttr(col, attr)
            col += 1

    # ------------------------------------------------------
    # begin the added code to manipulate the table (non wx related)
    def AppendRow(self, row):
        #print 'append'
        entry = {}

        for name in self.colnames:
            entry[name] = "Appended_%i"%row

        # XXX Hack
        # entry["A"] can only be between 1..4
        entry["A"] = random.choice(range(4))
        self.data.insert(row, ["Append_%i"%row, entry])

    def DeleteCols(self, cols):
        """
        cols -> delete the columns from the dataset
        cols hold the column indices
        """
        # we'll cheat here and just remove the name from the
        # list of column names.  The data will remain but
        # it won't be shown
        deleteCount = 0
        cols = cols[:]
        cols.sort()

        for i in cols:
            self.colnames.pop(i-deleteCount)
            # we need to advance the delete count
            # to make sure we delete the right columns
            deleteCount += 1

        if not len(self.colnames):
            self.data = []

    def DeleteRows(self, rows):
        """
        rows -> delete the rows from the dataset
        rows hold the row indices
        """
        deleteCount = 0
        rows = rows[:]
        rows.sort()

        for i in rows:
            self.data.pop(i-deleteCount)
            # we need to advance the delete count
            # to make sure we delete the right rows
            deleteCount += 1

    def SortColumn(self, col):
        """
        col -> sort the data based on the column indexed by col
        """
        name = self.colnames[col]
        _data = []

        for row in self.data:
            rowname, entry = row
            _data.append((entry.get(name, None), row))

        _data.sort()
        self.data = []

        for sortvalue, row in _data:
            self.data.append(row)

    # end table manipulation code
    # ----------------------------------------------------------


class OpalGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        self.books = list()
#         self.grid = wx.grid.Grid(self)
#         self.directory_name = '/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books'



    def loadBooks(self):
        print 'loadBooks'
#         self.books = list()
#         self.books=FindingBook().findAllBooks()
        numOfRows = 0
        if self.books:
            numOfRows = len(self.books)
            print 'numOfRows:', numOfRows
        self.CreateGrid(numOfRows, 10)

        # Enable Column moving
        gridmovers.GridColMover(self)
        self.Bind(gridmovers.EVT_GRID_COL_MOVE, self.OnColMove, self)

        self.SetRowLabelSize(30)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.showPopupMenu)
        self.SetColSize(0, 320)
        self.SetColSize(1, 220)
        self.SetColLabelValue(0, "Title")
        self.SetColLabelValue(1, "Author")
        self.SetColLabelValue(2, "publisher")
        self.SetColLabelValue(3, "isbn-13")
        self.SetColLabelValue(4, "size(MB)")
        self.SetColLabelValue(5, "Format")
        self.SetColLabelValue(6, "Path")
#         self.SetColLabelRenderer(0, MyCornerLabelRenderer(self))

        color = 'light gray'
        attr = self.cellAttr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(color)
        rowNum = 0
        for book in self.books:
            if rowNum % 2 == 0:
                for i in range(7):
                    self.SetAttr(rowNum, i, attr)
#             self.SetCellRenderer(rowNum, i,)
            self.SetCellValue(rowNum, 0, book.bookName)
            self.SetCellValue(rowNum, 1, book.authors[0].authorName)
            self.SetCellValue(rowNum, 2, book.publisher)
            self.SetCellValue(rowNum, 3, book.isbn_13)
            if book.fileSize:
                self.SetCellValue(rowNum, 4, book.fileSize)
            else:
                self.SetCellValue(rowNum, 4, '0')
            self.SetCellValue(rowNum, 5, book.bookFormat)
            self.SetCellValue(rowNum, 6, book.bookPath)
            rowNum = rowNum + 1
        pass


    def showPopupMenu(self, event):
        """
        Create and display a popup menu on right-click event
        """
        self.rowSelected = event.Row
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            # make a menu
            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnOpen, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OpenBook, id=self.popupID5)
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1, "Open book detail in New Tab.")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_MENU, (16, 16)))
        menu.AppendItem(item)

        item = wx.MenuItem(menu, self.popupID2, "Open containing folder.")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_MENU, (16, 16)))
        menu.AppendItem(item)

        item = wx.MenuItem(menu, self.popupID3, "Search similar books.")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_MENU, (16, 16)))
        menu.AppendItem(item)

        item = wx.MenuItem(menu, self.popupID4, "Properties.")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MENU, (16, 16)))
        menu.AppendItem(item)

        item = wx.MenuItem(menu, self.popupID5, "Open Book")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK, wx.ART_MENU, (16, 16)))
        menu.AppendItem(item)

#         menu.Append(self.popupID2, "Open containing folder.")
#         menu.Append(self.popupID3, "Search similar books.")
#         menu.Append(self.popupID4, "Properties.")
#         menu.Append(self.popupID5, "Open Book")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()



        # Event method called when a column move needs to take place
    def OnColMove(self,evt):
        frm = evt.GetMoveColumn()       # Column being moved
        to = evt.GetBeforeColumn()      # Before which column to insert

        print 'frm',frm
        print 'to',to
        grid = self.GetView()

        if grid:
            # Move the rowLabels and data rows
            oldLabel = self.rowLabels[frm]
            oldData = self.data[frm]
            del self.rowLabels[frm]
            del self.data[frm]

            if to > frm:
                self.rowLabels.insert(to-1,oldLabel)
                self.data.insert(to-1,oldData)
            else:
                self.rowLabels.insert(to,oldLabel)
                self.data.insert(to,oldData)

            # Notify the grid
            grid.BeginBatch()

            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, frm, 1
                    )

            grid.ProcessTableMessage(msg)

            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_INSERTED, to, 1
                    )

            grid.ProcessTableMessage(msg)
            grid.EndBatch()

    def OnPopupOne(self, event):
#         logger.info("Popup one\n")
        tabTitle = self.Parent.grid.GetCellValue(self.rowSelected, 0)
        path = self.Parent.grid.GetCellValue(self.rowSelected, 6)
        listOfDirPath = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
        self.path = ''
        for sName in listOfDirPath:
            if 'jpg' == sName.split('.')[-1:][0]:
                self.path = path + '/' + sName

        self.page = '''
            <html>
                <body>

                    <div>

                            <h1>Professional Java for Web Applications</h1>

                            <div>
                                <img src="''' + self.path + '''" alt="Professional Java for Web Applications" title="Professional Java for Web Applications" width="200"  />
                                <h3>Book Description</h3>
                                <p>
                                    This guide shows Java software developers and software engineers how to build complex web applications in an enterprise environment. You'll begin with an introduction to the Java Enterprise Edition and the basic web application, then set up a development application server environment, learn about the tools used in the development process, and explore numerous Java technologies and practices. The book covers industry-standard tools and technologies, specific technologies, and underlying programming concepts.
                                </p>
                            </div>

                        </div>
                </body>
            </html>
            '''


#         self.tabTwo = TabPanel(self.Parent.Parent)
#         html = wx.html.HtmlWindow(self.tabTwo, id=wx.ID_ANY, pos=(0, 0), size=wx.DisplaySize())
#
# #         html =  wx.webkit.web(self.tabTwo, id=wx.ID_ANY, pos=(0,0), size=(802,610))
#         if 'gtk2' in wx.PlatformInfo:
#             html.SetStandardFonts()
#         self.tabTwo.SetDoubleBuffered(True)
# #         self.t = wx.StaticText(self.tabTwo , -1, "This is a PageOne object", (20,20))
# #         html = wx.html.HtmlWindow(self.tabTwo, pos=(20,20))
#         html.SetPage(self.page)
# #         self.tabTwo.addHtml()
#         self.Parent.Parent.AddPage(self.tabTwo, tabTitle)

    def OpenBook(self, event):
#         logger.info("OpenBook\n")
        print self.rowSelected
#         self.grid=self.mainBookTab.tabOne.grid
        print 'directory_name:', self.directory_name
        FILE_NAME = ''
        FILE_NAME = "/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/3082/Tinkering.pdf"
        # self.
        os.spawnlp(os.P_NOWAIT, 'evince', 'evince', FILE_NAME)

    def OnOpen(self, event):

#         logger.info("Popup two\n")
        if sys.platform == 'win32':
            pass
#         import _winreg
#         path= r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon')
#         for root in (_winreg.HKEY_CURRENT_USER, _winreg.HKEY_LOCAL_MACHINE):
#             try:
#                 with _winreg.OpenKey(root, path) as k:
#                     value, regtype= _winreg.QueryValueEx(k, 'Shell')
#             except WindowsError:
#                 pass
#             else:
#                 if regtype in (_winreg.REG_SZ, _winreg.REG_EXPAND_SZ):
#                     shell= value
#                 break
#         else:grid
#             shell= 'Explorer.exe'
#         subprocess.Popen([shell, d])


    def OnPopupThree(self, event):
#         logger.info("Popup three\n")
        pass

    def OnPopupFour(self, event):
        FILE_NAME = "/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/3082/Tinkering.pdf"
#         import subprocess
#         subprocess.call(('cmd', '/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/3082', 'start', '', "Tinkering.pdf"))
        os.spawnlp(os.P_NOWAIT, 'evince', 'evince', FILE_NAME)
#         logger.info("Popup four\n")


class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "A Grid", size=(275, 275))
        grid = OpalGrid(self)
        grid.loadBooks()

if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = TestFrame(None)
    frame.Show(True)
    app.MainLoop()