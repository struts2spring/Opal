'''
Created on 14-Nov-2015

@author: vijay
'''

import wx
from src.ui.view.windowMgr import PyAUIFrame


class Main():

    def myMain(self):
        app = wx.App()
        frame = PyAUIFrame( None)
        frame.Show()
        app.MainLoop()


if __name__ == '__main__':
    Main().myMain()
    pass