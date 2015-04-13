import os
import sys
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin
import pyglet

song = "01 - Nothing But Trouble.mp3"
music = pyglet.resource.media(song)
info = MP3(song)

m, s = divmod(info.info.length, 60)
h, m = divmod(m, 60)

songs = {
1 : (info['TIT2'].text[0], info['TPE1'].text[0], "%d:%02d:%02d" % (h, m, s))
}


class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self, len(songs))
        self.itemDataMap = songs

    def GetListCtrl(self):
        return self
    
class Songs(wx.Frame):
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 500))

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        panel = wx.Panel(self, -1)

        
        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)     

        self.list = SortedListCtrl(rightPanel)
        self.list.InsertColumn(0, 'Title', width=140)
        self.list.InsertColumn(1, 'Artist', width=130)
        self.list.InsertColumn(2, 'Length', wx.LIST_FORMAT_RIGHT, 90)

        items = songs.items()

        for key, data in items:
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetStringItem(index, 1, data[1])
            self.list.SetStringItem(index, 2, data[2])
            self.list.SetItemData(index, key)


        vbox2 = wx.BoxSizer(wx.VERTICAL)

        sel = wx.Button(leftPanel, -1, 'Play/Pause', size=(100, -1))
        des = wx.Button(leftPanel, -1, 'Exit', size=(100, -1))


        self.Bind(wx.EVT_BUTTON, self.PlayPause, id=sel.GetId())
        self.Bind(wx.EVT_BUTTON, self.ExitApp, id=des.GetId())

        vbox2.Add(sel, 0, wx.TOP, 5)
        vbox2.Add(des)

        leftPanel.SetSizer(vbox2)

        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP, 3)
        vbox.Add((-1, 10))

        
        rightPanel.SetSizer(vbox)

        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add((3, -1))

        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)
        
    def PlayPause(self, event):
        music.play()
       
    def OnDoubleClick(self, event):
        if self.player.playing == False:
            music.play()
        else:
            music.pause()
        event.Skip()
        
    def OnSliderScroll(self, e):
        
        obj = e.GetEventObject()
        val = obj.GetValue()
        
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClick)
        

        
    def ExitApp(self, event):
        self.Close()

if __name__ == '__main__':
    player = pyglet.media.Player()
    app = wx.App()
    Songs(None, -1, 'PyTunes')
    app.MainLoop()


