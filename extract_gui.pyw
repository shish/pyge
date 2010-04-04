#!/usr/bin/python

import os, os.path, sys
import getopt, struct, re
import wx

from pyge import *
import pygelib

class ListPanel(wx.Panel):
    def __init__(self, parent, mainframe):
        wx.Panel.__init__(self, parent)
        self.mainframe = mainframe

        self.list = wx.ListCtrl(self,
                style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING)
        self.list.InsertColumn(0, "Filename")
        self.list.InsertColumn(1, "Size")
        self.list.SetColumnWidth(0, 256)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onExtract)
        
        lsizer = wx.BoxSizer(wx.VERTICAL)
        lsizer.Add(self.list, 1, flag=wx.EXPAND)
        self.SetSizerAndFit(lsizer)

    def setArchive(self, archive):
        self.archive = archive

        self.list.DeleteAllItems()
        self.archive.read()
        items = self.archive.list.items()
        items.sort()
        n = 0
        for key, data in items:
            self.mainframe.status.SetStatusText("Loading %s" % (data["name"]), 0)
            index = self.list.InsertStringItem(sys.maxint, data["name"])
            self.list.SetStringItem(index, 1, str(data["length"]/1024)+" KB")
            self.list.SetItemData(index, n)
            n = n + 1

        self.mainframe.status.SetStatusText("Ready", 0)

    def onExtract(self, evt):
        sdlg = self.mainframe.savedlg
        sddlg = self.mainframe.savedirdlg

        i = self.list.GetFirstSelected()
        files = []
        if i == -1:
            files = self.archive.list.keys()
        else:
            while i != -1:
                files.append(self.list.GetItemText(i))
                i = self.list.GetNextSelected(i)

        if len(files) == 1:
            sdlg.SetFilename(os.path.basename(files[0].replace("\\", "/")))
            if sdlg.ShowModal() == wx.ID_OK:
                target = open(sdlg.GetPath(), 'wb')
                self.archive.extract(files[0], target)
                target.close()
        else:
            if sddlg.ShowModal() == wx.ID_OK:
                n = 0
                dname = sddlg.GetPath()
                for fname in files:
                    self.mainframe.status.SetStatusText("Extracting %s" % (fname), 0)
                    n = n + 1
                    target = open(os.path.join(dname, fname), 'wb')
                    self.archive.extract(fname, target)
                    target.close()

        self.mainframe.status.SetStatusText("Ready")


class MyFrame(wx.Frame):
    archive = None
    file = None
    mode = None
    list = None
    sound = None
    opendlg = None
    savedlg = None
    savedirdlg = None
    layout = None

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(500, 400))

        self.plugins = pygelib.load_plugins("./plugins")

        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu 
        menu = wx.Menu()
        ID_EXTRACT = wx.NewId()
        menu.Append(wx.ID_OPEN, "&Open Archive", "Open an archive")
        self.Bind(wx.EVT_MENU, self.onOpenArchive, id=wx.ID_OPEN)
        menu.Append(ID_EXTRACT, "&Extract Files", "Extracts the selected files")
        self.Bind(wx.EVT_MENU, self.onExtract, id=ID_EXTRACT)
        menu.Append(wx.ID_EXIT, "E&xit", "Exit PyGE")
        self.Bind(wx.EVT_MENU, self.onTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        # status bar
        self.status = wx.StatusBar(self, style=0)
        self.status.SetFieldsCount(2)
        self.status.SetStatusWidths([-3, -1])
        self.status.SetStatusText("Ready", 0)
        self.SetStatusBar(self.status)

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)
        self.lpanel = ListPanel(panel, self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.lpanel, 1, flag=wx.EXPAND)
        panel.SetSizerAndFit(sizer)
        self.layout = sizer


        wcall = ""
        wclist = ""
#        for key in plugins:
#            type_, ext, class_ = formats[key]
#            wcall = wcall + ext + ";"
#            wclist = wclist + ("%s %s (%s)|%s|" % (key, type_, ext, ext))
#        wildcard = "All known formats|" + wcall + "|" + wclist + "All files|*.*"
        wildcard = "All files|*.*"
        self.opendlg = wx.FileDialog(self, message="Open Archive",
                wildcard=wildcard, defaultDir=os.getcwd(), style=wx.OPEN | wx.FILE_MUST_EXIST)
        self.savedlg = wx.FileDialog(self, message="Extract To",
                defaultDir=os.getcwd(), style=wx.SAVE | wx.OVERWRITE_PROMPT)
        self.savedirdlg = wx.DirDialog(self, message="Extract all into folder",
                defaultPath=os.getcwd(), style=wx.SAVE | wx.DD_NEW_DIR_BUTTON)

        self.panel = panel

    def onOpenArchive(self, evt):
        if self.opendlg.ShowModal() == wx.ID_OK:
            filename = self.opendlg.GetPath()
        else:
            return

        if self.file:
            self.file.close()
        self.file = open(filename, 'rb+')

        self.archive = None
        for plugin in self.plugins:
            if plugin(filename, self.file).detect():
                self.archive = plugin(filename, self.file)
                break

        if self.archive == None:
            dlg = wx.MessageDialog(self,
                    "The selected file isn't a supported archive type",
                    "Format not recognised", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self.lpanel.setArchive(self.archive)

        # if self.panel is shrunk, self.Fit() will shrink the whole window
        # if not, things are fit into the current size
        #self.panel.Fit()
        self.Fit()
        self.status.SetStatusText("Ready", 0)

    def onExtract(self, evt):
        self.lpanel.onExtract(evt)

    def onTimeToClose(self, evt):
        self.Close()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "Game Archive Extractor")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


if __name__ == "__main__":
    pye = MyApp(True)
    pye.MainLoop()

