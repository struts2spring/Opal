import  os
import  wx
import wx.html
import  wx.lib.filebrowsebutton as filebrowse
from src.static.constant import Workspace
from src.dao.BookDao import CreateDatabase
import logging

logger = logging.getLogger('extensive')
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------

class WorkspacePanel(wx.Panel):
    def __init__(self, parent, log=None):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.newPath = Workspace().path
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        hBox4 = wx.BoxSizer(wx.HORIZONTAL)

        page = '''
        <html>
        <body>
            <h4>Select a workspace</h4>
            Opal stores your books in a folder called workspace. \n
            Choose a workspace folder to use for this session.
        </body>
        </html>
        '''
        
        
        ctrl = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, size=(550, 100))
        if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
            ctrl.SetStandardFonts()
        ctrl.SetPage(page)

        self.info = wx.InfoBar(self)


# TODO
        self.dbb = filebrowse.DirBrowseButton(
            self, -1, size=(450, -1), changeCallback=self.dbbCallback, startDirectory=Workspace().path
            )
        print '----otherWorkspace------', Workspace().path
        if Workspace().path:
            self.dbb.textControl.SetValue(Workspace().path)


        okButton = wx.Button(self, -1, "OK")
        cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.okBtnClicked, okButton)
        self.Bind(wx.EVT_BUTTON, self.cancelBtnClicked, cancelButton)




        hBox2.Add(ctrl, 0, wx.ALL | wx.EXPAND, 5)
        vBox.Add(self.info, 0, wx.EXPAND)
        hBox4.Add(self.dbb, 0, wx.ALL | wx.EXPAND, 5)

        hBox3.Add(okButton, 0, wx.ALL | wx.RIGHT, 5)
        hBox3.Add(cancelButton, 0, wx.ALL | wx.RIGHT, 5)

        vBox.Add(hBox2, 0, wx.EXPAND)
        vBox.Add(hBox1, 0, wx.EXPAND)
        vBox.Add(hBox4, 0, wx.EXPAND)
        vBox.Add(hBox3, 0, wx.ALL | wx.RIGHT, 5)

        self.SetSizer(vBox)
        vBox.Fit(self)

    def dbbCallback(self, evt):
        print ('DirBrowseButton: %s\n' % evt.GetString())
        print os.path.isdir(evt.GetString())
        
        if not os.path.isdir(evt.GetString()):
            self.info.ShowMessage('This directory path does not exist. OK will create a new directory path.', wx.ICON_WARNING)
            self.newPath = evt.GetString()
        else:
            self.info.Dismiss()
        if os.path.isdir(evt.GetString()):
            os.chdir(evt.GetString())



    def EvtChoice(self, event):
        print ('EvtChoice: %s\n' % event.GetString())
        self.dirPath = event.GetString()

    def okBtnClicked(self, event):
        print 'okBtnClicked'
        
        if not os.path.exists(self.newPath):
            os.makedirs(self.newPath)
        if os.path.exists(self.newPath):
            os.chdir(self.newPath)
        print ("CWD: %s\n" % os.getcwd()),
        Workspace().path = os.getcwd()
        self.resetWorkspace()
        self.Parent.Destroy()
    def cancelBtnClicked(self, event):
        print 'cancelBtnClicked'
        self.Parent.Destroy()



    def resetWorkspace(self):
        os.chdir(Workspace().path)
        print '---resetWorkspace---->', os.getcwd()
        listOfDir = os.listdir(Workspace().path)
        if len(listOfDir) > 0:
    #         print len(listOfDir)
            isDatabase = False
            for sName in listOfDir:
                if ".sqlite" in str(sName):
                    print sName
                    isDatabase = True
            if not  isDatabase:
                createDatabase = CreateDatabase()
                session = createDatabase.creatingDatabase()
                createDatabase.addingData()





class WorkspaceFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(WorkspaceFrame, self).__init__(*args, **kwargs)
        panel = WorkspacePanel(self)

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = WorkspaceFrame(None, title='workspace')
    frame.Show()
    app.MainLoop()

