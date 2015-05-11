'''
#Title: Project 3- pyTunes
#Authors : Sean McCarthy and Nick Drinovsky
#Description: pyTunes(unofficial name) is a library of sound files. When you play a song, images relating to that song will display.
#Date: Week 17. 5/13/2015. 
'''


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
import time

pyglet.resource.path = ['./MP3s/']
pyglet.resource.reindex()

songs = {}


length = 0
currentdir = os.getcwd()


class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self, len(songs))
        self.itemDataMap = songs

    def GetListCtrl(self):
        return self

#This "Songs" class runs the actual frame for PyTunes 
class Songs(wx.Frame):
    artist_name = "Default"
    album_name = "Default"
    player = pyglet.media.Player()
    player.eos_action = player.EOS_PAUSE
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))
        
        '''
        Images addition to frame
        '''
         #find images in the image folder
        self.jpgs = GetJpgList("./IMAGES/" + self.artist_name + "/" + self.album_name)
        self.CurrentJpg = 0
        self.MaxImageSize = 200

        
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        
        #Add panels to the Frame
        panel = wx.Panel(self, -1)
        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)
        picPanel = wx.Panel(panel, -1)

        #draw an empty image box that we will replace with files from the IMAGES folder

        self.Image = wx.StaticBitmap(picPanel, bitmap = wx.EmptyBitmap(self.MaxImageSize, self.MaxImageSize))

        self.SHOWNEXT()

        self.list = SortedListCtrl(rightPanel)

        self.list.InsertColumn(0, 'Title', width=140)
        self.list.InsertColumn(1, 'Artist', width=140)
        self.list.InsertColumn(2, 'Album', width=140)
        self.list.InsertColumn(3, 'Length', wx.LIST_FORMAT_RIGHT, 90)

        #Song metadata pull here?
        items = songs.items()

        for key, data in items:
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetStringItem(index, 1, data[1])
            self.list.SetStringItem(index, 2, data[2])
            self.list.SetStringItem(index, 3, data[3])
            self.list.SetItemData(index, key)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClick, self.list)

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        #Create buttons and place them in the left panel
        ply = wx.Button(leftPanel, -1, 'Play', size=(100, -1))
        pse = wx.Button(leftPanel, -1, 'Pause', size=(100, -1))
        stp = wx.Button(leftPanel, -1, 'Stop', size=(100, -1))
        ext = wx.Button(leftPanel, -1, 'Exit', size=(100, -1))
        nextpic = wx.Button(leftPanel, -1, "Next Picture", size = (100, -1))
        
        #slider addition here
        slid = wx.Slider(rightPanel, -1, value = 0, minValue = 0, maxValue = 500, pos = (-1,-1), size = (250,-1), style = wx.SL_AUTOTICKS | wx.SL_LABELS)
        slid.SetTickFreq(50,1)

        
        self.Bind(wx.EVT_BUTTON, self.Play, id=ply.GetId())
        self.Bind(wx.EVT_BUTTON, self.Pause, id=pse.GetId())
        self.Bind(wx.EVT_BUTTON, self.Stop, id=stp.GetId())
        self.Bind(wx.EVT_BUTTON, self.ExitApp, id=ext.GetId())
        self.Bind(wx.EVT_BUTTON, self.SHOWNEXT, id = nextpic.GetId())
        self.Bind(wx.EVT_SCROLL, self.OnSlideScroll)

        self.CurrentTime()

    
        vbox2.Add(ply, 0, wx.TOP, 5)
        vbox2.Add(pse)
        vbox2.Add(stp)
        vbox2.Add(ext)
        vbox2.Add(nextpic)

        leftPanel.SetSizer(vbox2)

        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP, 3)
        vbox.Add(slid, 1, wx.EXPAND)
        vbox.Add((-1, 10))

         
        rightPanel.SetSizer(vbox)

        
        
        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add(picPanel, 2)
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
        
    def Stop(self, event):
        self.player.pause()
        self.player = pyglet.media.Player()
           
    def OnDoubleClick(self, event):
        self.player.pause()
        self.player = pyglet.media.Player()
        os.chdir('./MP3s/')
        selection = self.list.GetFocusedItem()
        music = songs[selection]
        song = music[4]
        s = pyglet.resource.media(song)
        self.player.queue(s)
        self.player.play()
        os.chdir(currentdir)
        self.artist_name = music[1]
        self.album_name = music[2]
        if (os.path.exists("./IMAGES/" + self.artist_name + "/" + self.album_name)):
            self.jpgs = GetJpgList("./IMAGES/" + self.artist_name + "/" + self.album_name)
            self.Image.Update()
            self.SHOWNEXT()
        else:
            self.artist_name = "Default"
            self.album_name = "Default"
            self.jpgs = GetJpgList("./IMAGES/" + self.artist_name + "/" + self.album_name)
            self.Image.Update()
            self.SHOWNEXT()
            
    def OnSlideScroll(self, event):
        self.current_time = 0
        
    def ExitApp(self, event):
        self.player.pause()
        self.Close()


    def CurrentTime(self):
        while self.player.play():
            time.sleep(1)
            self.current_time = self.current_time + 1

            val = self.current_time

            txt1.SetLabel(str(val))
            
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
        
        self.Refresh

        #Run through the list of images and if the last image is reached, start over
        self.CurrentJpg += 1
        if self.CurrentJpg > len(self.jpgs) - 1:
            self.CurrentJpg = 0

def GetJpgList(dir):
    jpgs = [f for f in os.listdir(dir) if f[-4:] == ".jpg"]
    return [os.path.join(dir, f) for f in jpgs]


def GetMP3List(dict, dir):
        mp3 = [f for f in os.listdir(dir) if f[-4:] == ".mp3"]
        os.chdir(dir)
        y = len(mp3)
        x = 0
        while x < y:
            music = MP3(mp3[x])
            m, s = divmod(music.info.length, 60)
            h, m = divmod(m, 60)
            songs[x] =(music['TIT2'].text[0], music['TPE1'].text[0], music['TALB'].text[0], "%d:%02d:%02d" % (h, m, s),  (mp3[x]))
            x += 1
        os.chdir(currentdir)

if __name__ == '__main__':
    GetMP3List(songs, "./MP3s/")
    app = wx.App()
    Songs(None, -1, 'pyTunes')
    app.MainLoop()
