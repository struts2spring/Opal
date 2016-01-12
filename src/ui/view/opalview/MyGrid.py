
import  wx
import  wx.grid as  Grid

# import  images
import random
from src.logic.search_book import FindingBook
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import sys
import subprocess

#---------------------------------------------------------------------------

class MegaTable(Grid.PyGridTableBase):
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
        Grid.PyGridTableBase.__init__(self)
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
#         print 'GetValue:', self.GetColLabelValue(col)
        value=str(self.data[row][1].get(self.GetColLabelValue(col), ""))
        if 'authors'== self.GetColLabelValue(col):
            author=''
            for a in self.data[row][1].get(self.GetColLabelValue(col), ""):
                author  = author+a.authorName+'\n'
            value=author
        return value

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
            (self._rows, self.GetNumberRows(), Grid.GRIDTABLE_NOTIFY_ROWS_DELETED, Grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
            (self._cols, self.GetNumberCols(), Grid.GRIDTABLE_NOTIFY_COLS_DELETED, Grid.GRIDTABLE_NOTIFY_COLS_APPENDED),
        ]:

            if new < current:
                msg = Grid.GridTableMessage(self,delmsg,new,current-new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = Grid.GridTableMessage(self,addmsg,new-current)
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
        msg = Grid.GridTableMessage(self, Grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
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
            attr = Grid.GridCellAttr()
            color = 'light gray'
#         attr = self.cellAttr = wx.grid.GridCellAttr()
#             attr.SetBackgroundColour(color)
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


# --------------------------------------------------------------------
# Sample wx.Grid renderers

class MegaImageRenderer(Grid.PyGridCellRenderer):
    def __init__(self, table):
        """
        Image Renderer Test.  This just places an image in a cell
        based on the row index.  There are N choices and the
        choice is made by  choice[row%N]
        """
        Grid.PyGridCellRenderer.__init__(self)
        self.table = table



        self._choices = {'pdf': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep +"pdf.png"),
                         'chm': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep +"chm.png"),
                         'mobi': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep +"mobi.png"),
                         'epub': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep +"epub.png"),
                         'doc': wx.Bitmap(os.path.dirname(__file__) + os.sep + "images" + os.sep +"doc.png")
                         }

        self.colSize = None
        self.rowSize = None

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        choice = self.table.GetRawValue(row, col)
        bmp= self._choices.get(choice.lower())
#         print 'Draw.choice:',choice
        # create the blank bitmap as a draw background
#         bmp=wx.Bitmap("/home/vijay/Documents/Aptana_Workspace/util/src/ui/view/opalview/images/pdf.png")
        image = wx.MemoryDC()
        image.SelectObject(bmp)

        # clear the background
        dc.SetBackgroundMode(wx.SOLID)

#         if isSelected:
#             dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
#             dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
#         else:
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangleRect(rect)


        # copy the image but only to the size of the grid cell
#         width, height = bmp.GetWidth(), bmp.GetHeight()
        width, height = bmp.GetWidth(),bmp.GetHeight()

        if width > rect.width-2:
            width = rect.width-2

        if height > rect.height-2:
            height = rect.height-2

        dc.Blit(rect.x+1, rect.y+1, width, height,
                image,
                0, 0, wx.COPY, True)


class MegaFontRenderer(Grid.PyGridCellRenderer):
    def __init__(self, table, color="light blue", font="ARIAL", fontsize=8):
        """Render data in the specified color and font and fontsize"""
        Grid.PyGridCellRenderer.__init__(self)
        self.table = table
        self.color = color
        self.font = wx.Font(fontsize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, font)
        self.selectedBrush = wx.Brush("light blue", wx.SOLID)
        self.normalBrush = wx.Brush(wx.WHITE, wx.SOLID)
        self.colSize = None
        self.rowSize = 50

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        # Here we draw text in a grid cell using various fonts
        # and colors.  We have to set the clipping region on
        # the grid's DC, otherwise the text will spill over
        # to the next cell
        dc.SetClippingRect(rect)

        # clear the background
        dc.SetBackgroundMode(wx.SOLID)

#         if isSelected:
#             dc.SetBrush(wx.Brush(wx.LIGHT_GREY_BRUSH, wx.SOLID))
#             dc.SetPen(wx.Pen(wx.LIGHT_GREY_BRUSH, 1, wx.SOLID))
#         else:
#             dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
#             dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangleRect(rect)

        text = self.table.GetValue(row, col)
        dc.SetBackgroundMode(wx.SOLID)

        # change the text background based on whether the grid is selected
        # or not
        if isSelected:
            dc.SetBrush(self.selectedBrush)
            dc.SetTextBackground("light blue")
        else:
            dc.SetBrush(self.normalBrush)
            dc.SetTextBackground("white")

        dc.SetTextForeground(self.color)
        dc.SetFont(self.font)
        dc.DrawText(text, rect.x+1, rect.y+1)

        # Okay, now for the advanced class :)
        # Let's add three dots "..."
        # to indicate that that there is more text to be read
        # when the text is larger than the grid cell

        width, height = dc.GetTextExtent(text)

        if width > rect.width-2:
            width, height = dc.GetTextExtent("...")
            x = rect.x+1 + rect.width-2 - width
            dc.DrawRectangle(x, rect.y+1, width+1, height)
            dc.DrawText("...", x, rect.y+1)

        dc.DestroyClippingRegion()


# --------------------------------------------------------------------
# Sample Grid using a specialized table and renderers that can
# be plugged in based on column names

class MegaGrid(Grid.Grid):
    def __init__(self, parent, data, colnames):
        plugins={"bookName":MegaFontRendererFactory("red", "ARIAL", 8),
                                        "bookFormat":MegaImageRenderer,
                                        "Test":MegaFontRendererFactory("orange", "TIMES", 24),}
        """parent, data, colnames, plugins=None
        Initialize a grid using the data defined in data and colnames
        (see MegaTable for a description of the data format)
        plugins is a dictionary of columnName -> column renderers.
        """

        # The base class must be initialized *first*
        Grid.Grid.__init__(self, parent, -1)
        self._table = MegaTable(data, colnames, plugins)
        self.SetTable(self._table)
        self._plugins = plugins

        self.Bind(Grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClicked)
        self.Bind(Grid.EVT_GRID_CELL_RIGHT_CLICK, self.showPopupMenu)

    def Reset(self):
        """reset the view based on the data in the table.  Call
        this when rows are added or destroyed"""
        self._table.ResetView(self)

    def OnLabelRightClicked(self, evt):
        # Did we click on a row or a column?
        row, col = evt.GetRow(), evt.GetCol()
        if row == -1: self.colPopup(col, evt)
        elif col == -1: self.rowPopup(row, evt)

    def rowPopup(self, row, evt):
        """(row, evt) -> display a popup menu when a row label is right clicked"""
        appendID = wx.NewId()
        deleteID = wx.NewId()
        x = self.GetRowSize(row)/2

        if not self.GetSelectedRows():
            self.SelectRow(row)

        menu = wx.Menu()
        xo, yo = evt.GetPosition()
        menu.Append(appendID, "Append Row")
        menu.Append(deleteID, "Delete Row(s)")

        def append(event, self=self, row=row):
            self._table.AppendRow(row)
            self.Reset()

        def delete(event, self=self, row=row):
            rows = self.GetSelectedRows()
            self._table.DeleteRows(rows)
            self.Reset()

        self.Bind(wx.EVT_MENU, append, id=appendID)
        self.Bind(wx.EVT_MENU, delete, id=deleteID)
        self.PopupMenu(menu, (x, yo))
        menu.Destroy()
        return


    def colPopup(self, col, evt):
        """(col, evt) -> display a popup menu when a column label is
        right clicked"""
        x = self.GetColSize(col)/2
        menu = wx.Menu()
        id1 = wx.NewId()
        sortID = wx.NewId()

        xo, yo = evt.GetPosition()
        self.SelectCol(col)
        cols = self.GetSelectedCols()
        self.Refresh()
        menu.Append(id1, "Delete Col(s)")
        menu.Append(sortID, "Sort Column")

        def delete(event, self=self, col=col):
            cols = self.GetSelectedCols()
            self._table.DeleteCols(cols)
            self.Reset()

        def sort(event, self=self, col=col):
            self._table.SortColumn(col)
            self.Reset()

        self.Bind(wx.EVT_MENU, delete, id=id1)

        if len(cols) == 1:
            self.Bind(wx.EVT_MENU, sort, id=sortID)

        self.PopupMenu(menu, (xo, 0))
        menu.Destroy()
        return

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
            self.popupID6 = wx.NewId()
            # make a menu
            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnOpenFolderPath, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OpenBook, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.deleteBook, id=self.popupID6)
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

        item = wx.MenuItem(menu, self.popupID6, "Delete Book")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU, (16, 16)))
        menu.AppendItem(item)

#         menu.Append(self.popupID2, "Open containing folder.")
#         menu.Append(self.popupID3, "Search similar books.")
#         menu.Append(self.popupID4, "Properties.")
#         menu.Append(self.popupID5, "Open Book")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def OnPopupOne(self, event):
        print ("Popup one\n")
    def deleteBook(self, event):
        print ("delete Book\n")

    def OnOpenFolderPath(self, event):
        print ("OnOpenFolderPath \n")
        print self.rowSelected
        if self.rowSelected != None:
            book=self._table.data[self.rowSelected][1]
            print self.rowSelected
            file=book['bookPath']
        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", file])
        elif sys.platform == 'win32':
            os.startfile(file)

    def OnPopupThree(self, event):
        print ("OnPopupThree \n")

    def OnPopupFour(self, event):
        print ("OnPopupFour \n")

    def OpenBook(self, event):
        print self.rowSelected
        if self.rowSelected !=None:
            book=self._table.data[self.rowSelected][1]
            print self.rowSelected
            bookPath=book['bookPath']
            for name in os.listdir(bookPath):
                if ".pdf" in name:
                    print name
                    file=os.path.join(bookPath,name)
                elif  ".epub" in name:
                    file=os.path.join(bookPath,name)

        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", file])
        elif sys.platform == 'win32':
            os.startfile(file)
        print ("OpenBook \n")

class MegaFontRendererFactory:
    def __init__(self, color, font, fontsize):
        """
        (color, font, fontsize) -> set of a factory to generate
        renderers when called.
        func = MegaFontRenderFactory(color, font, fontsize)
        renderer = func(table)
        """
        self.color = color
        self.font = font
        self.fontsize = fontsize

    def __call__(self, table):
        return MegaFontRenderer(table, self.color, self.font, self.fontsize)


# -----------------------------------------------------------------
# Test data
# data is in the form
# [rowname, dictionary]
# where dictionary.get(colname, None) -> returns the value for the cell
#
# the colname must also be supplied



# for row in range(100000):
#     d = {}
# #     books=FindingBook().findAllBooks()
# #     print books
# #     for b in books:
# #         print b
# #         print '-------------'
# #         break
#     for name in ["This", "Test", "Is"]:
#         d[name] = random.random()
#
#     d["Row"] = len(data)
#     # XXX
#     # the "A" column can only be between one and 4
#     d["A"] = random.choice(range(4))
#     data.append((str(row), d))
class TestFrame(wx.Frame):
    def __init__(self, parent,):
        wx.Frame.__init__(self, parent, -1,
                         "Test Frame", size=(640,480))
        import random

        books=FindingBook().searchingBook('flex')

        colnames = [ 'id','bookName', 'bookFormat']
        # for b in books:
        #     colnames=b.__dict__.keys()
        #     break



        data = []
        bookId_rowNo_dict={}
        noOfBooks=len(books)
        for i in range(noOfBooks):
#             colnames=books[i].__dict__.keys()
#             print colnames
            d = {}
            data.append((str(i), books[i].__dict__))
            bookId_rowNo_dict[books[i].id]=i
        grid = MegaGrid(self, data, colnames)
        grid.bookId_rowNo_dict=bookId_rowNo_dict
        grid.Reset()
        grid.SelectRow(row=3)

if __name__=='__main__':
    app = wx.App()
    frame = TestFrame(None)
    frame.Show(True)
    app.MainLoop()