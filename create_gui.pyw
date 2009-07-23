#!/usr/bin/python

import os, os.path, sys
import getopt, struct, re
import wx

from pyge import *

class MyFrame(wx.Frame):
    list = None
    archive = None
    srcdir = "./"

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(500, 400))

        self.opendirdlg = wx.DirDialog(self, message="Select Source Directory",
                defaultPath=os.getcwd(), style=wx.OPEN)
        self.savedlg = wx.FileDialog(self, message="Save As",
                defaultDir=os.getcwd(), style=wx.SAVE | wx.OVERWRITE_PROMPT)

        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu 
        menu = wx.Menu()
        ID_CREATE = wx.NewId()
        menu.Append(wx.ID_OPEN, "O&pen Directory\tAlt-O", "Open a source directory")
        self.Bind(wx.EVT_MENU, self.onOpenDirectory, id=wx.ID_OPEN)
        menu.Append(ID_CREATE, "C&reate Archive\tAlt-C", "Create an archive")
        self.Bind(wx.EVT_MENU, self.onCreateArchive, id=ID_CREATE)
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")
        self.Bind(wx.EVT_MENU, self.onTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()

        panel = wx.Panel(self, -1)
        tID = wx.NewId()
        self.list = wx.ListCtrl(panel, tID,
                style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING)
        self.list.InsertColumn(0, "Filename")
        self.list.InsertColumn(1, "Size")


        sizer = wx.GridBagSizer(3, 3)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(0)
        sizer.Add(self.list, (0, 0), (2, 3), flag=wx.EXPAND)
        panel.SetSizerAndFit(sizer)
        sizer.Layout()
        panel.Layout()

    def onOpenDirectory(self, evt):
        self.list.DeleteAllItems()

        if self.opendirdlg.ShowModal() == wx.ID_OK:
            srcdir = self.opendirdlg.GetPath()
            os.chdir(srcdir)

            self.archive = FileSystemArchive(".", None)
            self.archive.read()
            items = self.archive.list.items()
            n = 0
            for key, data in items:
                index = self.list.InsertStringItem(sys.maxint, data["name"])
                self.list.SetStringItem(index, 1, str(data["length"]/1024)+" KB")
                self.list.SetItemData(index, n)
                n = n + 1

    def onCreateArchive(self, evt):
        if self.archive == None:
            dlg = wx.MessageDialog(self,
                    "Please select a source directory",
                    "No Source Directory", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return

        fmt = ""
        dlg = wx.SingleChoiceDialog(
                self, 'Choose which format to use', 'Select Format',
                formats.keys(), wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            fmt = dlg.GetStringSelection()
        else:
            return
        dlg.Destroy()

        if self.savedlg.ShowModal() == wx.ID_OK:
            fname = self.savedlg.GetPath()
            fp = open(fname, 'wb+')
            archive = formats[fmt][2](fname, fp)
            flist = self.archive.list.keys()
            flist.sort()
            archive.create(flist)
            fp.close()

    def onTimeToClose(self, evt):
        self.Close()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "Game Archive Creator")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == "__main__":
    pye = MyApp(True)
    pye.MainLoop()

