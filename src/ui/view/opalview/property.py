
import sys, time, math, os, os.path

import wx
import wx.richtext
from src.logic.search_book import FindingBook
import datetime
from src.static.imgUtil import ImageUtil
from src.logic.ReadWriteJson import Book, ReadWriteJsonInfo, Author
import threading
from src.ui.view.opalview.RichTextCtrlPanel import RichTextPanel
from sys import exc_info

_ = wx.GetTranslation
import wx.propgrid as wxpg
import logging

logger = logging.getLogger('extensive')


############################################################################
#
# TEST RELATED CODE AND VARIABLES
#
############################################################################

default_object_content2 = """\
object.title = "Object Title"
object.index = 1
object.PI = %f
object.wxpython_rules = True
""" % (math.pi)

default_object_content1 = """\

#
# Note that the results of autofill will appear on the second page.

#
# Set number of iterations appropriately to test performance
iterations = 100

#
# Test result for 100,000 iterations on Athlon XP 2000+:
#
# Time spent per property: 0.054ms
# Memory allocated per property: ~350 bytes (includes Python object)
#

for i in range(0,iterations):
    setattr(object,'title%i'%i,"Object Title")
    setattr(object,'index%i'%i,1)
    setattr(object,'PI%i'%i,3.14)
    setattr(object,'wxpython_rules%i'%i,True)
"""


############################################################################
#
# CUSTOM PROPERTY SAMPLES
#
############################################################################


class ValueObject:
    def __init__(self):
        pass


class IntProperty2(wxpg.PyProperty):
    """\
    This is a simple re-implementation of wxIntProperty.
    """
    def __init__(self, label, name=wxpg.LABEL_AS_NAME, value=0):
        wxpg.PyProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        """\
        This is not 100% necessary and in future is probably going to be
        automated to return class name.
        """
        return "IntProperty2"

    def GetEditor(self):
        return "TextCtrl"

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, s, flags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        try:
            v = int(s)
            if self.GetValue() != v:
                return (True, v)
        except (ValueError, TypeError):
            if flags & wxpg.PG_REPORT_ERROR:
                wx.MessageBox("Cannot convert '%s' into a number." % s, "Error")
        return False

    def IntToValue(self, v, flags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        if (self.GetValue() != v):
            return (True, v)
        return False

    def ValidateValue(self, value, validationInfo):
        """ Let's limit the value to range -10000 and 10000.
        """
        # Just test this function to make sure validationInfo and
        # wxPGVFBFlags work properly.
        oldvfb__ = validationInfo.GetFailureBehavior()

        # Mark the cell if validaton failred
        validationInfo.SetFailureBehavior(wxpg.PG_VFB_MARK_CELL)

        if value < -10000 or value > 10000:
            return False

        return (True, value)


class SizeProperty(wxpg.PyProperty):
    """ Demonstrates a property with few children.
    """
    def __init__(self, label, name=wxpg.LABEL_AS_NAME, value=wx.Size(0, 0)):
        wxpg.PyProperty.__init__(self, label, name)

        value = self._ConvertValue(value)

        self.AddPrivateChild(wxpg.IntProperty("X", value=value.x))
        self.AddPrivateChild(wxpg.IntProperty("Y", value=value.y))

        self.m_value = value

    def GetClassName(self):
        return self.__class__.__name__

    def GetEditor(self):
        return "TextCtrl"

    def RefreshChildren(self):
        size = self.m_value
        self.Item(0).SetValue(size.x)
        self.Item(1).SetValue(size.y)

    def _ConvertValue(self, value):
        """ Utility convert arbitrary value to a real wx.Size.
        """
        from operator import isSequenceType
        if isinstance(value, wx.Point):
            value = wx.Size(value.x, value.y)
        elif isSequenceType(value):
            value = wx.Size(*value)
        return value

    def ChildChanged(self, thisValue, childIndex, childValue):
        # FIXME: This does not work yet. ChildChanged needs be fixed "for"
        #        wxPython in wxWidgets SVN trunk, and that has to wait for
        #        2.9.1, as wxPython 2.9.0 uses WX_2_9_0_BRANCH.
        size = self._ConvertValue(self.m_value)
        if childIndex == 0:
            size.x = childValue
        elif childIndex == 1:
            size.y = childValue
        else:
            raise AssertionError

        return size


class DirsProperty(wxpg.PyArrayStringProperty):
    """ Sample of a custom custom ArrayStringProperty.

        Because currently some of the C++ helpers from wxArrayStringProperty
        and wxProperytGrid are not available, our implementation has to quite
        a bit 'manually'. Which is not too bad since Python has excellent
        string and list manipulation facilities.
    """
    def __init__(self, label, name=wxpg.LABEL_AS_NAME, value=[]):
        wxpg.PyArrayStringProperty.__init__(self, label, name, value)

        # Set default delimiter
        self.SetAttribute("Delimiter", ',')

    def GetEditor(self):
        return "TextCtrlAndButton"

    def ValueToString(self, value, flags):
        return self.m_display

    def OnSetValue(self):
        self.GenerateValueAsString()

    def DoSetAttribute(self, name, value):
        # Proper way to call same method from super class
        retval = self.CallSuperMethod("DoSetAttribute", name, value)

        #
        # Must re-generate cached string when delimiter changes
        if name == "Delimiter":
            self.GenerateValueAsString(delim=value)

        return retval

    def GenerateValueAsString(self, delim=None):
        """ This function creates a cached version of displayed text
            (self.m_display).
        """
        if not delim:
            delim = self.GetAttribute("Delimiter")
            if not delim:
                delim = ','

        ls = self.GetValue()
        if delim == '"' or delim == "'":
            text = ' '.join(['%s%s%s' % (delim, a, delim) for a in ls])
        else:
            text = ', '.join(ls)
        self.m_display = text

    def StringToValue(self, text, argFlags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        delim = self.GetAttribute("Delimiter")
        if delim == '"' or delim == "'":
            # Proper way to call same method from super class
            return self.CallSuperMethod("StringToValue", text, 0)
        v = [a.strip() for a in text.split(delim)]
        return (True, v)

    def OnEvent(self, propgrid, primaryEditor, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            dlg = wx.DirDialog(propgrid,
                               _("Select a directory to be added to "
                                 "the list:"))

            if dlg.ShowModal() == wx.ID_OK:
                new_path = dlg.GetPath()
                old_value = self.m_value
                if old_value:
                    new_value = list(old_value)
                    new_value.append(new_path)
                else:
                    new_value = [new_path]
                self.SetValueInEvent(new_value)
                retval = True
            else:
                retval = False

            dlg.Destroy()
            return retval

        return False


class PyObjectPropertyValue:
    """\
    Value type of our sample PyObjectProperty. We keep a simple dash-delimited
    list of string given as argument to constructor.
    """
    def __init__(self, s=None):
        try:
            self.ls = [a.strip() for a in s.split('-')]
        except:
            self.ls = []

    def __repr__(self):
        return ' - '.join(self.ls)


class PyObjectProperty(wxpg.PyProperty):
    """\
    Another simple example. This time our value is a PyObject.

    NOTE: We can't return an arbitrary python object in DoGetValue. It cannot
          be a simple type such as int, bool, double, or string, nor an array
          or wxObject based. Dictionary, None, or any user-specified Python
          class is allowed.
    """
    def __init__(self, label, name=wxpg.LABEL_AS_NAME, value=None):
        wxpg.PyProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        return self.__class__.__name__

    def GetEditor(self):
        return "TextCtrl"

    def ValueToString(self, value, flags):
        return repr(value)

    def StringToValue(self, s, flags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        v = PyObjectPropertyValue(s)
        return (True, v)


class SampleMultiButtonEditor(wxpg.PyTextCtrlEditor):
    def __init__(self):
        wxpg.PyTextCtrlEditor.__init__(self)

    def CreateControls(self, propGrid, property, pos, sz):
        # Create and populate buttons-subwindow
        buttons = wxpg.PGMultiButton(propGrid, sz)

        # Add two regular buttons
        buttons.AddButton("...")
        buttons.AddButton("A")
        # Add a bitmap button
        x = ImageUtil()
        buttons.AddBitmapButton(x.getBitmap(iconName='pdf', size=(10, 10)))
        
        # Create the 'primary' editor control (textctrl in this case)
        wnd = self.CallSuperMethod("CreateControls",
                                   propGrid,
                                   property,
                                   pos,
                                   buttons.GetPrimarySize())

        # Finally, move buttons-subwindow to correct position and make sure
        # returned wxPGWindowList contains our custom button list.
        buttons.Finalize(propGrid, pos);

        # We must maintain a reference to any editor objects we created
        # ourselves. Otherwise they might be freed prematurely. Also,
        # we need it in OnEvent() below, because in Python we cannot "cast"
        # result of wxPropertyGrid.GetEditorControlSecondary() into
        # PGMultiButton instance.
        self.buttons = buttons

        return (wnd, buttons)

    def OnEvent(self, propGrid, prop, ctrl, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            buttons = self.buttons
            evtId = event.GetId()

            if evtId == buttons.GetButtonId(0):
                # Do something when the first button is pressed
                wx.LogDebug("First button pressed");
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(1):
                # Do something when the second button is pressed
                wx.MessageBox("Second button pressed");
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(2):
                # Do something when the third button is pressed
                wx.MessageBox("Third button pressed");
                return False  # Return false since value did not change

        return self.CallSuperMethod("OnEvent", propGrid, prop, ctrl, event)


class SingleChoiceDialogAdapter(wxpg.PyEditorDialogAdapter):
    """ This demonstrates use of wxpg.PyEditorDialogAdapter.
    """
    def __init__(self, choices):
        wxpg.PyEditorDialogAdapter.__init__(self)
        self.choices = choices

    def DoShowDialog(self, propGrid, property):
        s = wx.GetSingleChoice("Message", "Caption", self.choices)

        if s:
            self.SetValue(s)
            return True

        return False;


class SingleChoiceProperty(wxpg.PyStringProperty):
    def __init__(self, label, name=wxpg.LABEL_AS_NAME, value=''):
        wxpg.PyStringProperty.__init__(self, label, name, value)

        # Prepare choices
        dialog_choices = []
        dialog_choices.append("Cat");
        dialog_choices.append("Dog");
        dialog_choices.append("Gibbon");
        dialog_choices.append("Otter");

        self.dialog_choices = dialog_choices

    def GetEditor(self):
        # Set editor to have button
        return "TextCtrlAndButton"

    def GetEditorDialog(self):
        # Set what happens on button click
        return SingleChoiceDialogAdapter(self.dialog_choices)


class TrivialPropertyEditor(wxpg.PyEditor):
    """\
    This is a simple re-creation of TextCtrlWithButton. Note that it does
    not take advantage of wx.TextCtrl and wx.Button creation helper functions
    in wx.PropertyGrid.
    """
    def __init__(self):
        wxpg.PyEditor.__init__(self)

    def CreateControls(self, propgrid, property, pos, sz):
        """ Create the actual wxPython controls here for editing the
            property value.

            You must use propgrid.GetPanel() as parent for created controls.

            Return value is either single editor control or tuple of two
            editor controls, of which first is the primary one and second
            is usually a button.
        """
        try:
            x, y = pos
            w, h = sz
            h = 64 + 6

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            s = property.GetDisplayedString();

            tc = wx.TextCtrl(propgrid.GetPanel(), wxpg.PG_SUBID1, s,
                             (x, y), (w, h),
                             wx.TE_PROCESS_ENTER)
            btn = wx.Button(propgrid.GetPanel(), wxpg.PG_SUBID2, '...',
                            (x + w, y),
                            (bw, h), wx.WANTS_CHARS)
            return (tc, btn)
        except:
            import traceback
            print(traceback.print_exc())

    def UpdateControl(self, property, ctrl):
        ctrl.SetValue(property.GetDisplayedString())

    def DrawValue(self, dc, rect, property, text):
        if not property.IsValueUnspecified():
            dc.DrawText(property.GetDisplayedString(), rect.x + 5, rect.y)

    def OnEvent(self, propgrid, property, ctrl, event):
        """ Return True if modified editor value should be committed to
            the property. To just mark the property value modified, call
            propgrid.EditorsValueWasModified().
        """
        if not ctrl:
            return False

        evtType = event.GetEventType()

        if evtType == wx.wxEVT_COMMAND_TEXT_ENTER:
            if propgrid.IsEditorsValueModified():
                return True
        elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED:
            #
            # Pass this event outside wxPropertyGrid so that,
            # if necessary, program can tell when user is editing
            # a textctrl.
            event.Skip()
            event.SetId(propgrid.GetId())

            propgrid.EditorsValueWasModified()
            return False

        return False

    def GetValueFromControl(self, property, ctrl):
        """ Return tuple (wasSuccess, newValue), where wasSuccess is True if
            different value was acquired succesfully.
        """
        tc = ctrl
        textVal = tc.GetValue()

        if property.UsesAutoUnspecified() and not textVal:
            return (True, None)

        res, value = property.StringToValue(textVal,
                                            wxpg.PG_EDITABLE_VALUE)

        # Changing unspecified always causes event (returning
        # True here should be enough to trigger it).
        if not res and value is None:
            res = True

        return (res, value)

    def SetValueToUnspecified(self, property, ctrl):
        ctrl.Remove(0, len(ctrl.GetValue()))

    def SetControlStringValue(self, property, ctrl, text):
        ctrl.SetValue(text)

    def OnFocus(self, property, ctrl):
        ctrl.SetSelection(-1, -1)
        ctrl.SetFocus()


class LargeImagePickerCtrl(wx.Panel):
    """\
    Control created and used by LargeImageEditor.
    """
    def __init__(self):
        pre = wx.PrePanel()
        self.PostCreate(pre)

    def Create(self, parent, id_, pos, size, style=0):
        wx.Panel.Create(self, parent, id_, pos, size,
                        style | wx.BORDER_SIMPLE)
        img_spc = size[1]
        self.tc = wx.TextCtrl(self, -1, "", (img_spc, 0), (2048, size[1]),
                              wx.BORDER_NONE)
        self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.property = None
        self.bmp = None
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        whiteBrush = wx.Brush(wx.WHITE)
        dc.SetBackground(whiteBrush)
        dc.Clear()

        bmp = self.bmp
        if bmp:
            dc.DrawBitmap(bmp, 2, 2)
        else:
            dc.SetPen(wx.Pen(wx.BLACK))
            dc.SetBrush(whiteBrush)
            dc.DrawRectangle(2, 2, 64, 64)

    def RefreshThumbnail(self):
        """\
        We use here very simple image scaling code.
        """
        if not self.property:
            self.bmp = None
            return

        path = self.property.DoGetValue()

        if not os.path.isfile(path):
            self.bmp = None
            return

        image = wx.Image(path)
        image.Rescale(64, 64)
        self.bmp = wx.BitmapFromImage(image)

    def SetProperty(self, property):
        self.property = property
        self.tc.SetValue(property.GetDisplayedString())
        self.RefreshThumbnail()

    def SetValue(self, s):
        self.RefreshThumbnail()
        self.tc.SetValue(s)

    def GetLastPosition(self):
        return self.tc.GetLastPosition()


class LargeImageEditor(wxpg.PyEditor):
    """\
    Double-height text-editor with image in front.
    """
    def __init__(self):
        wxpg.PyEditor.__init__(self)

    def CreateControls(self, propgrid, property, pos, sz):
        try:
            x, y = pos
            w, h = sz
            h = 64 + 6

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            lipc = LargeImagePickerCtrl()
            if sys.platform.startswith('win'):
                lipc.Hide()
            lipc.Create(propgrid.GetPanel(), wxpg.PG_SUBID1, (x, y), (w, h))
            lipc.SetProperty(property)
            btn = wx.Button(propgrid.GetPanel(), wxpg.PG_SUBID2, '...',
                            (x + w, y),
                            (bw, h), wx.WANTS_CHARS)
            return (lipc, btn)
        except:
            import traceback
            print(traceback.print_exc())

    def UpdateControl(self, property, ctrl):
        ctrl.SetValue(property.GetDisplayedString())

    def DrawValue(self, dc, rect, property, text):
        if not property.IsValueUnspecified():
            dc.DrawText(property.GetDisplayedString(), rect.x + 5, rect.y)

    def OnEvent(self, propgrid, property, ctrl, event):
        """ Return True if modified editor value should be committed to
            the property. To just mark the property value modified, call
            propgrid.EditorsValueWasModified().
        """
        if not ctrl:
            return False

        evtType = event.GetEventType()

        if evtType == wx.wxEVT_COMMAND_TEXT_ENTER:
            if propgrid.IsEditorsValueModified():
                return True
        elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED:
            #
            # Pass this event outside wxPropertyGrid so that,
            # if necessary, program can tell when user is editing
            # a textctrl.
            event.Skip()
            event.SetId(propgrid.GetId())

            propgrid.EditorsValueWasModified()
            return False

        return False

    def GetValueFromControl(self, property, ctrl):
        """ Return tuple (wasSuccess, newValue), where wasSuccess is True if
            different value was acquired succesfully.
        """
        tc = ctrl.tc
        textVal = tc.GetValue()

        if property.UsesAutoUnspecified() and not textVal:
            return (None, True)

        res, value = property.StringToValue(textVal,
                                            wxpg.PG_EDITABLE_VALUE)

        # Changing unspecified always causes event (returning
        # True here should be enough to trigger it).
        if not res and value is None:
            res = True

        return (res, value)

    def SetValueToUnspecified(self, property, ctrl):
        ctrl.tc.Remove(0, len(ctrl.tc.GetValue()))

    def SetControlStringValue(self, property, ctrl, txt):
        ctrl.SetValue(txt)

    def OnFocus(self, property, ctrl):
        ctrl.tc.SetSelection(-1, -1)
        ctrl.tc.SetFocus()

    def CanContainCustomImage(self):
        return True


############################################################################
#
# MAIN PROPERTY GRID TEST PANEL
#
############################################################################
class PropertyPhotoPanel(wx.Panel):

    def __init__(self, parent=None, book=None):
        wx.Panel.__init__(self, parent, id=-1)
        self.Bind(wx.EVT_SIZE, self.OnSize, self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.parent = parent
        self.bitmap = None
        self.currentBook = book
        
    def OnContextMenu(self, event):
        print("OnContextMenu\n")

        # only do this part the first time so the events are only bound once
        #
        # Yet another anternate way to do IDs. Some prefer them up top to
        # avoid clutter, some prefer them close to the object of interest
        # for clarity. 
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1, "Copy book cover")
#         bmp = images.Smiles.GetBitmap()
#         item.SetBitmap(bmp)
        menu.AppendItem(item)
        # add some other items
        menu.Append(self.popupID2, "Download book cover")
        menu.Append(self.popupID3, "Generate book cover")
        menu.Append(self.popupID4, "Open book")
        
        
        self.Bind(wx.EVT_MENU, self.OnCopyToClipboard, id=self.popupID1)
        self.Bind(wx.EVT_MENU, self.downloadCover, id=self.popupID2)
        self.Bind(wx.EVT_MENU, self.generateCover, id=self.popupID3)
        self.Bind(wx.EVT_MENU, self.openBook, id=self.popupID4)
        
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
    def downloadCover(self, event):
        print 'downloadCover'
    def generateCover(self, event):
        print 'generateCover'
    def openBook(self, event):
        print 'openBook'        
        
    def OnCopyToClipboard(self, event):
        print 'OnCopyToClipboard'

        d = wx.BitmapDataObject(self.bitmap)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(d)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
            print("Image copied to cliboard.\n")
        else:
            print("Couldn't open clipboard!\n")  
              
    def OnSize(self, event):
        try:
            self.changeBitmapWorker()
        except Exception as e:
            logger.error(e, exc_info=True)

    def OnPaint(self, evt):
        if self.bitmap != None:
            dc = wx.BufferedPaintDC(self)
            dc.Clear()
            dc.DrawBitmap(self.bitmap, 0, 0)
        else:
            pass
    def changeBitmapWorker(self):
#         relevant_path = "/docs/LiClipse Workspace/img/wallpaper"
#         imgFileName=self.getImgFileName(relevant_path)
#         imgFilePath=os.path.join(relevant_path,imgFileName[0] )
        imgFilePath = os.path.join(self.currentBook.bookPath, self.currentBook.bookImgName)
#         img2 =  imgFilePath=os.path.join(relevant_path,imgFileName[1] )
        logger.debug('size: %s', self.GetSize())
        NewW, NewH = self.GetSize()
        if  NewW > 0 and NewH > 0:
            img = wx.Image(imgFilePath, wx.BITMAP_TYPE_ANY)
            img = img.Scale(NewW, NewH)
            self.bitmap = wx.BitmapFromImage(img)
#             self.Refresh()
        
        
#     def getImgFileName(self, relevant_path=None):
#     #         relevant_path = "/docs/LiClipse Workspace/img/wallpaper"
#         included_extenstions = ['jpg', 'bmp', 'png', 'gif']
#         file_names = [fn for fn in os.listdir(relevant_path)
#                       if any(fn.endswith(ext) for ext in included_extenstions)]
#         return file_names
class BookPropertyPanel(wx.Panel):

    def __init__(self, parent, book):
        wx.Panel.__init__(self, parent)

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.currentBook = book
        
        self.photoPanel = PropertyPhotoPanel(self, book=self.currentBook)
#         self.rt = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)
        self.rt = RichTextPanel(self, book)
#         img1 = wx.Image(os.path.join(self.currentBook.bookPath, self.currentBook.bookImgName), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
#         img=wx.Bitmap(os.path.join(book.bookPath, book.bookImgName))
        logger.debug('BookPropertyPanel size: %s', self.GetParent().GetSize())
        try:
            img1 = self.scale_bitmap()
        except Exception as e:
            logger.error(e, exc_info=True)
        img = wx.EmptyImage(240, 240)

#         self.imageCtrl = wx.StaticBitmap(self.photoPanel, wx.ID_ANY, wx.BitmapFromImage(img))
#         self.imageCtrl = wx.StaticBitmap(self.photoPanel, wx.ID_ANY, img1, name="anotherEmptyImage")
#         self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.onImageClick)
        
        
        topsizer = wx.BoxSizer(wx.VERTICAL)
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.pg = self.createPropetyGrid(self.currentBook)
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(self.pg, 1, wx.EXPAND, 2)
        vBox.Add(self.rt, 1, wx.EXPAND, 1)
        hBox.Add(vBox, 3, wx.EXPAND, 5)
        hBox.Add(self.photoPanel, 2, wx.EXPAND, 1)
        
        topsizer.Add(hBox, 3, wx.EXPAND)
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        next = wx.Button(self.panel, -1, "Next")
        previous = wx.Button(self.panel, -1, "Previous")
        cancel = wx.Button(self.panel, -1, "Cancel")
        ok = wx.Button(self.panel, -1, "Ok")
        downloadMetadata = wx.Button(self.panel, -1, "Download metadata")
        downloadCover = wx.Button(self.panel, -1, "Download cover")
        generateCover = wx.Button(self.panel, -1, "Generate cover")
        
        next.Bind(wx.EVT_BUTTON, self.onNext)
        previous.Bind(wx.EVT_BUTTON, self.onPrevious)
        ok.Bind(wx.EVT_BUTTON, self.onOk)
        cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        downloadMetadata.Bind(wx.EVT_BUTTON, self.onDownloadMetadata)
        downloadCover.Bind(wx.EVT_BUTTON, self.onDownloadCover)
        generateCover.Bind(wx.EVT_BUTTON, self.onGenerateCover)
        
        
        
        rowsizer.Add(previous, 1)
        rowsizer.Add(next, 1)
        rowsizer.Add(cancel, 1)
        rowsizer.Add(ok, 1)
        rowsizer.Add(downloadMetadata, 1)
        rowsizer.Add(downloadCover, 1)
        rowsizer.Add(generateCover, 1)
        topsizer.Add(rowsizer, 0, wx.EXPAND)


        self.panel.SetSizer(topsizer)
        topsizer.SetSizeHints(self.panel)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.sizer.Fit(self)
        self.SetSizer(self.sizer)
#         self.SetAutoLayout(True)

    #----------------------------------------------------------------------
    

        
    def scale_bitmap(self, width=None, height=None):
        bitmap = wx.Image(os.path.join(self.currentBook.bookPath, self.currentBook.bookImgName), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image = wx.ImageFromBitmap(bitmap)
        if width and height:
            image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result
    
    def onNext(self, event):
        logger.debug('onNext')
        bookId = self.currentBook.id
        self.previousBook = self.currentBook
        b = FindingBook().findBookByNextMaxId(bookId)
        if b:
            self.currentBook = b
            self.setValuesToPropetyGrid()
            self.photoPanel.currentBook = b
            self.photoPanel.changeBitmapWorker()
            if b.bookDescription != None:
                self.rt.rtc.ChangeValue(b.bookDescription)
        
        
    def onPrevious(self, event):
        logger.debug('onPrevious')
        bookId = self.currentBook.id
        self.previousBook = self.currentBook
        b = FindingBook().findBookByPreviousMaxId(bookId)
        if b:
            self.currentBook = b
            self.setValuesToPropetyGrid()
            self.photoPanel.currentBook = b
            self.photoPanel.changeBitmapWorker()
            if b.bookDescription != None:
                self.rt.rtc.ChangeValue(b.bookDescription)
        
    def onOk(self, event):
        logger.debug('onOk')
#         props = self.pg.GetPropertyValues(inc_attributes=True)
        self.save()
        self.GetParent().OnCloseFrame(event)
#         self.GetParent().OnCloseFrame(event)
#         print props['Book name']
    def save(self):
        props = self.pg.GetPropertyValues(inc_attributes=True)
        self.setValuesToBookFromPropertyGrid(props)
    def onCancel(self, event):
        logger.debug('onCancel')   
        self.GetParent().OnCloseFrame(event)
    
    def onDownloadMetadata(self, event):
        logger.debug('onDownloadMetadata') 
          
    def onDownloadCover(self, event):
        logger.debug('onDownloadCover')
    
    def onGenerateCover(self, event):
        logger.debug('onGenerateCover')    
    
    def setValuesToPropetyGrid(self):
        '''
        This method is used to set values in property grid.
        '''
#         self.imageCtrl.SetBitmap(wx.Image(os.path.join(self.currentBook.bookPath, self.currentBook.bookImgName), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        props = self.pg.GetPropertyValues(inc_attributes=True)
        props['id'] = self.currentBook.id
        
        props['id'] = self.currentBook.id
        props['Book name'] = str(self.currentBook.bookName or '')
        props['Book description'] = str(self.currentBook.bookDescription or '')
        props['Number of pages'] = str(self.currentBook.numberOfPages or '')
        
        authorName = list()
        for a in self.currentBook.authors:
            authorName.append(a.authorName)
        props['Author(s) name'] = ','.join(authorName)
        props['Rating'] = str(self.currentBook.rating or 0)
        props['Tag'] = str(self.currentBook.id or '')
        props['File location'] = str(self.currentBook.bookPath or '')
        props['File size'] = str(self.currentBook.fileSize or '')
        props['file Format'] = str(self.currentBook.bookFormat or '')
        
        imgPath = os.path.join(self.currentBook.bookPath, self.currentBook.bookImgName)
        props['Book image'] = imgPath
        props['Publisher'] = str(self.currentBook.publisher or '')
        props['ISBN'] = str(self.currentBook.isbn_13 or '')
        props['Language'] = str(self.currentBook.inLanguage or '')
        
        self.pg.SetPropertyValues(props)
        self.Layout()

    def setValuesToBookFromPropertyGrid(self, props):
        book = Book()
#         props['id'] = self.currentBook.id
        book.publisher = props['Publisher']
        book.subTitle = self.currentBook.subTitle
        book.bookName = props['Book name']
        book.numberOfPages = props['Number of pages']
        book.bookDescription = self.rt.rtc.GetValue()
        book.authors = list()
        if props['Author(s) name']:
            authors = props['Author(s) name'].split(',')
            for a in authors:
                if a != '':
                    author = Author(authorName=a)
                    book.authors.append(author)
                
        book.rating = props['Rating']
#         book.bookPath = str(self.currentBook.bookPath or '')
        book.fileSize = props['File size'] 
        
#         props['Tag'] = str(self.currentBook.id or '')
        book.bookFormat = str(self.currentBook.bookFormat or '')
        
        book.bookImgName = self.currentBook.bookImgName
        if str(props['ISBN']) == '':
            book.isbn_13 = None
        else:
            book.isbn_13 = str(props['ISBN'])
        book.itEbookUrlNumber = self.currentBook.itEbookUrlNumber
        book.publishedOn = self.currentBook.publishedOn
        book.inLanguage = props['Language']
        ReadWriteJsonInfo().writeJsonToDir(self.currentBook.bookPath, book)
        
        
        
    def onImageClick(self, event):
        """"""
        print event.GetPosition(), 'onImageClick'
        imgCtrl = event.GetEventObject()
        print imgCtrl.GetName()
        
    def createPropetyGrid(self, book):
        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = wxpg.PropertyGridManager(self.panel,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER | 
#                               wxpg.PG_AUTO_SORT | 
                              wxpg.PG_TOOLBAR)

        # Show help as tooltips
#         pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        self.pg.Bind(wxpg.EVT_PG_CHANGED, self.OnPropGridChange)
        self.pg.Bind(wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange)
        self.pg.Bind(wxpg.EVT_PG_SELECTED, self.OnPropGridSelect)
        self.pg.Bind(wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick)


        #
        # Let's use some simple custom editor
        #
        # NOTE: Editor must be registered *before* adding a property that
        # uses it.
        if not getattr(sys, '_PropGridEditorsRegistered', False):
            self.pg.RegisterEditor(TrivialPropertyEditor)
            self.pg.RegisterEditor(SampleMultiButtonEditor)
            self.pg.RegisterEditor(LargeImageEditor)
            # ensure we only do it once
            sys._PropGridEditorsRegistered = True

        #
        # Add properties
        #

        self.pg.AddPage("Page 1 - Testing All")

        self.pg.Append(wxpg.PropertyCategory("1 - Basic Properties"))
        
        
        self.pg.Append(wxpg.StringProperty("Book name", value=book.bookName))
#         self.pg.Append(wxpg.StringProperty("Book description", value=str(book.bookDescription or '')))
        authorNames = list()
        if hasattr(book, 'authors'):
            for a in book.authors:
                authorNames.append(a.authorName)
        
        self.pg.Append(wxpg.StringProperty("Author(s) name", value=','.join(authorNames)))
        
        self.pg.Append(wxpg.StringProperty("Number of pages", value=str(book.numberOfPages or '')))
        self.pg.Append(wxpg.IntProperty("Rating", value=long(book.rating or 0)))
        self.pg.SetPropertyEditor("Rating", "SpinCtrl")
        
        self.pg.Append(wxpg.EditEnumProperty("Tag", "EditEnumProperty",
                                         ['Physis', 'B', 'C'],
                                         [0, 1, 2],
                                         "Text Not in List"))
        

        
        try:
            self.pg.Append(wxpg.StringProperty("Publisher", value=str(book.publisher or '')))
        except:
            pass
        self.pg.Append(wxpg.StringProperty("ISBN", value=str(book.isbn_13 or '')))
        self.pg.Append(wxpg.StringProperty("Language", value=str(book.inLanguage or '')))
        
        self.pg.Append(wxpg.PropertyCategory("2 - More Properties"))
        self.pg.Append(wxpg.IntProperty("id", value=book.id))
        self.pg.Append(wxpg.DirProperty("File location", value=book.bookPath))
        self.pg.Append(wxpg.StringProperty("File size", value=str(book.fileSize or '')))
        self.pg.Append(wxpg.LongStringProperty("MultipleButtons"));
        self.pg.SetPropertyEditor("MultipleButtons", "SampleMultiButtonEditor");
        
        imgPath = os.path.join(book.bookPath, book.bookImgName)
        self.pg.Append(wxpg.ImageFileProperty(label="Book image", value=imgPath))
#         self.pg.Append(wxpg.DateProperty("Published date", value=self.pydate2wxdate(book.publishedOn)))
       
        
        return self.pg


    def pydate2wxdate(self, date):
        assert isinstance(date, (datetime.datetime, datetime.date))
        tt = date.timetuple()
        dmy = (tt[2], tt[1] - 1, tt[0])
        return wx.DateTimeFromDMY(*dmy)
     
    def wxdate2pydate(self, date):
        assert isinstance(date, wx.DateTime)
        if date.IsValid():
            ymd = map(int, date.FormatISODate().split('-'))
            return datetime.date(*ymd)
        else:
            return None


    def OnPropGridChange(self, event):
        p = event.GetProperty()
        if p:
            logger.debug('%s changed to "%s"\n' , p.GetName(), p.GetValueAsString())

    def OnPropGridSelect(self, event):
        p = event.GetProperty()
        if p:
            logger.debug('%s selected\n' ,event.GetProperty().GetName())
        else:
            logger.debug('Nothing selected\n')

    def OnDeleteProperty(self, event):
        p = self.pg.GetSelectedProperty()
        if p:
            self.pg.DeleteProperty(p)
        else:
            wx.MessageBox("First select a property to delete")

    def OnReserved(self, event):
        pass

    def OnSetPropertyValues(self, event):
        try:
            d = self.pg.GetPropertyValues(inc_attributes=True)

            ss = []
            for k, v in d.iteritems():
                v = repr(v)
                if not v or v[0] != '<':
                    if k.startswith('@'):
                        ss.append('setattr(obj, "%s", %s)' % (k, v))
                    else:
                        ss.append('obj.%s = %s' % (k, v))

            dlg = MemoDialog(self,
                    "Enter Content for Object Used in SetPropertyValues",
                    '\n'.join(ss))  # default_object_content1

            if dlg.ShowModal() == wx.ID_OK:
                import datetime
                sandbox = {'obj':ValueObject(),
                           'wx':wx,
                           'datetime':datetime}
                exec dlg.tc.GetValue() in sandbox
                t_start = time.time()
                # print(sandbox['obj'].__dict__)
                self.pg.SetPropertyValues(sandbox['obj'])
                t_end = time.time()
                print('SetPropertyValues finished in %.0fms\n' % 
                               ((t_end - t_start) * 1000.0))
        except Exception as e:
            logger.error(e, exc_info=True)

    def OnGetPropertyValues(self, event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(inc_attributes=True)
            t_end = time.time()
            print('GetPropertyValues finished in %.0fms\n' % 
                           ((t_end - t_start) * 1000.0))
            ss = ['%s: %s' % (k, repr(v)) for k, v in d.iteritems()]
            dlg = MemoDialog(self, "GetPropertyValues Result",
                             'Contents of resulting dictionary:\n\n' + '\n'.join(ss))
            dlg.ShowModal()
        except Exception as e:
            logger.error(e, exc_info=True)

    def OnGetPropertyValues2(self, event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(as_strings=True)
            t_end = time.time()
            print('GetPropertyValues(as_strings=True) finished in %.0fms\n' % 
                           ((t_end - t_start) * 1000.0))
            ss = ['%s: %s' % (k, repr(v)) for k, v in d.iteritems()]
            dlg = MemoDialog(self, "GetPropertyValues Result",
                             'Contents of resulting dictionary:\n\n' + '\n'.join(ss))
            dlg.ShowModal()
        except Exception as e:
            logger.error(e, exc_info=True)

    def OnAutoFill(self, event):
        try:
            dlg = MemoDialog(self, "Enter Content for Object Used for AutoFill", default_object_content1)
            if dlg.ShowModal() == wx.ID_OK:
                sandbox = {'object':ValueObject(), 'wx':wx}
                exec dlg.tc.GetValue() in sandbox
                t_start = time.time()
                self.pg.AutoFill(sandbox['object'])
                t_end = time.time()

        except Exception as e:
            logger.error(e, exc_info=True)

    def OnPropGridRightClick(self, event):
        p = event.GetProperty()
        if p:
            print('%s right clicked\n' % (event.GetProperty().GetName()))
        else:
            print('Nothing right clicked\n')

    def OnPropGridPageChange(self, event):
        index = self.pg.GetSelectedPage()
        print('Page Changed to \'%s\'\n' % (self.pg.GetPageName(index)))

    def RunTests(self, event):
        pg = self.pg
        log = self.log

        # Validate client data
        print('Testing client data set/get')
        pg.SetPropertyClientData("Bool", 1234)
        if pg.GetPropertyClientData("Bool") != 1234:
            raise ValueError("Set/GetPropertyClientData() failed")

        # Test setting unicode string
        print('Testing setting an unicode string value')
        pg.GetPropertyByName("String").SetValue(u"Some Unicode Text")

        #
        # Test some code that *should* fail (but not crash)
        try:
            if wx.GetApp().GetAssertionMode() == wx.PYAPP_ASSERT_EXCEPTION:
                print('Testing exception handling compliancy')
                a_ = pg.GetPropertyValue("NotARealProperty")
                pg.EnableProperty("NotAtAllRealProperty", False)
                pg.SetPropertyHelpString("AgaintNotARealProperty",
                                         "Dummy Help String")
        except Exception as e:
            logger.error(e, exc_info=True)

        # GetPyIterator
        print('GetPage(0).GetPyIterator()\n')
        it = pg.GetPage(0).GetPyIterator(wxpg.PG_ITERATE_ALL)
        for prop in it:
            print('Iterating \'%s\'\n' % (prop.GetName()))

        # VIterator
        print('GetPyVIterator()\n')
        it = pg.GetPyVIterator(wxpg.PG_ITERATE_ALL)
        for prop in it:
            print('Iterating \'%s\'\n' % (prop.GetName()))

        # Properties
        print('GetPage(0).Properties\n')
        it = pg.GetPage(0).Properties
        for prop in it:
            print('Iterating \'%s\'\n' % (prop.GetName()))

        # Items
        print('GetPage(0).Items\n')
        it = pg.GetPage(0).Items
        for prop in it:
            print('Iterating \'%s\'\n' % (prop.GetName()))

#---------------------------------------------------------------------------
class MainNotebook(wx.Notebook):
    # ## For this demo, we don't need to subclass
    # ## Notebook at all.
    def __init__(self, parent, book):
        wx.Notebook.__init__(self, parent=parent)
        self.AddPage(BookPropertyPanel(self, book), 'book')
#         self.AddPage(RedPanel(self),"Red")

class MemoDialog(wx.Dialog):
    """\
    Dialog for multi-line text editing.
    """
    def __init__(self, parent=None, title="", text="", pos=None, size=(500, 500)):
        wx.Dialog.__init__(self, parent, -1, title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        topsizer = wx.BoxSizer(wx.VERTICAL)

        tc = wx.TextCtrl(self, 11, text, style=wx.TE_MULTILINE)
        self.tc = tc
        topsizer.Add(tc, 1, wx.EXPAND | wx.ALL, 8)

        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        rowsizer.Add(wx.Button(self, wx.ID_OK, 'Ok'), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL, 8)
        rowsizer.Add((0, 0), 1, wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL, 8)
        rowsizer.Add(wx.Button(self, wx.ID_CANCEL, 'Cancel'), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL, 8)
        topsizer.Add(rowsizer, 0, wx.EXPAND | wx.ALL, 8)

        self.SetSizer(topsizer)
        topsizer.Layout()

        self.SetSize(size)
        if not pos:
            self.CenterOnScreen()
        else:
            self.Move(pos)

#----------------------------------------------------------------------

# def runTest( frame, nb, log ):
#     win = TestPanel( nb, log )
#     return win

#----------------------------------------------------------------------


overview = """\
<html><body>
<P>
This demo shows all basic wxPropertyGrid properties, in addition to
some custom property classes.
</body></html>
"""


class BookPropertyFrame(wx.Frame):
    def __init__(self, parent, book):
        wx.Frame.__init__(self, parent, -1, title='Edit Book Metadata', size=(1100, 650))
        self.Notebook = MainNotebook(self, book)
        
#         self.panel = BookPropertyPanel(self, book)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
#         self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Show()
    # Makes sure the user was intending to quit the application
    def OnCloseFrame(self, event):
        self.OnExitApp(event)
        
    # Destroys the main frame which quits the wxPython application
    def OnExitApp(self, event):
        self.Destroy()
if __name__ == '__main__':
    books = FindingBook().findAllBooks()
    book = None
    for b in books:
        book = b
        break
    print book
    app = wx.App(0)
    frame = BookPropertyFrame(None, book)
    app.MainLoop() 

