import wx
import wx.media
import os

class MediaPlayerPanel(wx.Panel):
    def __init__(self, parent,id):
        wx.Panel.__init__(self,parent,-1,style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)
        self.SetBackgroundColour("#BCFFCD")

        try:
            self.mc = wx.media.MediaCtrl(self)
        except NotImplementedError:
            self.Destroy()
            raise # program exit.
        self.mc.SetVolume(0.5)
        self.doLoadFile('「あぁ～！フロア熱狂の音ォ ！！」.mp4')
        playButton = wx.Button(self, wx.ID_ANY, ' ')
        self.Bind(wx.EVT_BUTTON, self.onPlay, playButton)

    def doLoadFile(self, path):
        self.mc.Load(path)
        #self.mc.Play()

    def onPlay(self, evt):
        self.mc.Play()

def main():
    app = wx.App()
    frame = wx.Frame(None, -1, "play audio and video files", size = (500, 500))
    MediaPlayerPanel(frame, -1)
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()