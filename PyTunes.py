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
    player = pyglet.media.Player()
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))

        
        '''
        Images addition to frame
        '''
         #find images in the image folder
        self.artist_name = "Phantogram"
        self.jpgs = GetJpgList("./IMAGES/" + self.artist_name)
        self.CurrentJpg = 0

        self.MaxImageSize = 200

        
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        

        


        
        
        panel = wx.Panel(self, -1)
        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)
        picPanel = wx.Panel(panel, -1)

        #draw an empty image box that we will replace with files from the IMAGES folder

        self.Image = wx.StaticBitmap(picPanel, bitmap = wx.EmptyBitmap(self.MaxImageSize, self.MaxImageSize))

        self.SHOWNEXT()

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClick)
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

        ply = wx.Button(leftPanel, -1, 'Play', size=(100, -1))
        pse = wx.Button(leftPanel, -1, 'Pause', size=(100, -1))
        ext = wx.Button(leftPanel, -1, 'Exit', size=(100, -1))
        nextpic = wx.Button(leftPanel, -1, "Next Picture", size = (100, -1))
        


        self.Bind(wx.EVT_BUTTON, self.Play, id=ply.GetId())
        self.Bind(wx.EVT_BUTTON, self.Pause, id=pse.GetId())
        self.Bind(wx.EVT_BUTTON, self.ExitApp, id=ext.GetId())
        self.Bind(wx.EVT_BUTTON, self.SHOWNEXT, id = nextpic.GetId())

        vbox2.Add(ply, 0, wx.TOP, 5)
        vbox2.Add(pse)
        vbox2.Add(ext)
        vbox2.Add(nextpic)

        leftPanel.SetSizer(vbox2)

        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP, 3)
        vbox.Add((-1, 10))

         
        rightPanel.SetSizer(vbox)

        
        
        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add(picPanel, 2, wx.EXPAND)
        hbox.Add((3, -1))

        
        
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        
        picPanel.SetSizer(vbox3)
        
        vbox3.Add((1,1),1)
        vbox3.Add(self.Image, 0, wx.EXPAND | wx.RIGHT, 5)
        vbox3.Add((1,1),1)
        
        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)
        
    def Play(self, event):
        self.player.play()
        event.Skip()

    def Pause(self, event):
        self.player.pause()
        event.Skip()

    def OnDoubleClick(self, event):
        self.player.queue(music)
        
    def ExitApp(self, event):
        self.Close()

    def SHOWNEXT(self, event = None):
        PIC = wx.Image(self.jpgs[self.CurrentJpg], wx.BITMAP_TYPE_JPEG)

        W = PIC.GetWidth()
        H = PIC.GetHeight()
        if W > H:
            NewW = self.MaxImageSize
            NewH = self.MaxImageSize * H / W
        else:
            NewH = self.MaxImageSize
            NewW = self.MaxImageSize * W / H
        PIC = PIC.Scale(NewW,NewH)

        #Go from image to bitmap

        self.Image.SetBitmap(wx.BitmapFromImage(PIC))

        #self.Fit()
        #self.Layout()
        self.Refresh

        #Run through the list of images and if the last image is reached, start over
        self.CurrentJpg += 1
        if self.CurrentJpg > len(self.jpgs) - 1:
            self.CurrentJpg = 0

def GetJpgList(dir):
    jpgs = [f for f in os.listdir(dir) if f[-4:] == ".jpg"]
    # print "JPGS are:", jpgs
    return [os.path.join(dir, f) for f in jpgs]

if __name__ == '__main__':
    player = pyglet.media.Player()
    app = wx.App()
    Songs(None, -1, 'PyTunes')
    app.MainLoop()




