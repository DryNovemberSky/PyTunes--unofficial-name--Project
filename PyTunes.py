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


example_song = MP3("01 - Nothing But Trouble.mp3")

m, s = divmod(example_song.info.length, 60)
h, m = divmod(m, 60)

songs = {
1 : (example_song['TIT2'].text[0], example_song['TPE1'].text[0], "%d:%02d:%02d" % (h, m, s))
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
        wx.Frame.__init__(self, parent, id, title, size=(380, 230))
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        panel = wx.Panel(self, -1)
        
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClick)
        
        self.list = SortedListCtrl(panel)
        self.list.InsertColumn(0, 'Title', width=140)
        self.list.InsertColumn(1, 'Artist', width=130)
        self.list.InsertColumn(2, 'Length', wx.LIST_FORMAT_RIGHT, 90)

        items = songs.items()

        for key, data in items:
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetStringItem(index, 1, data[1])
            self.list.SetStringItem(index, 2, data[2])
            self.list.SetItemData(index, key)


        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)
        
    def OnDoubleClick(self, event):
        if pyglet.media.Player.playing == True:
            player.pause()
        music = pyglet.resource.media('01 - Nothing But Trouble.mp3')
        music.play()
        event.Skip()

app = wx.App()
Songs(None, -1, 'PyTunes')
app.MainLoop()


