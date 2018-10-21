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

        loadButton = wx.Button(self, wx.ID_ANY, "Load File")
        self.Bind(wx.EVT_BUTTON, self.onLoadFile, loadButton)

        playButton = wx.Button(self, wx.ID_ANY, "Play")
        playButton.SetToolTip(wx.ToolTip("load a file first")) # message when on mouse
        self.Bind(wx.EVT_BUTTON, self.onPlay, playButton)

        pauseButton = wx.Button(self, wx.ID_ANY, "Pause")
        pauseButton.SetToolTip(wx.ToolTip("press Play to resume"))
        self.Bind(wx.EVT_BUTTON, self.onPause, pauseButton)

        stopButton = wx.Button(self, wx.ID_ANY, "Stop")
        stopButton.SetToolTip(wx.ToolTip("also resets to start"))
        self.Bind(wx.EVT_BUTTON, self.onStop, stopButton)

        self.slider = wx.Slider(self, wx.ID_ANY, 1000000, 0, 1000000,
            size=(410, -1),
            style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)
        self.slider.Bind(wx.EVT_SLIDER, self.onSeek)

        ext = "load .mp3 .mpg .mid .wav .wma .au or .avi files"
        self.st_info = wx.StaticText(self, wx.ID_ANY, ext, size=(300,-1))

        sizer = wx.GridBagSizer(vgap=5, hgap=5)
        sizer.Add(loadButton, pos=(1,1))
        sizer.Add(self.st_info, pos=(1,2), span=(1,2))
        sizer.Add(self.slider, pos=(2,1), span=(2,3))
        sizer.Add(playButton, pos=(4,1))
        sizer.Add(pauseButton, pos=(4,2))
        sizer.Add(stopButton, pos=(4,3))
        # for .avi or .mpg video files use lower grid area
        sizer.Add(self.mc, pos=(5,1), span=(7,3))
        self.SetSizer(sizer)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        # update every 100 milliseconds
        self.timer.Start(100)

    def onLoadFile(self, evt):
        mask = "Media Files|*.mp3;*.mpg;*.mid;*.wav;*.au;*.avi|All (.*)|*.*"
        dlg = wx.FileDialog(self,
            message="Choose a media file (.mp3 .mpg .mid .wav .wma .au .avi)",
            defaultDir=os.getcwd(), defaultFile="",
            wildcard=mask)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.doLoadFile(path)
        dlg.Destroy()

    def doLoadFile(self, path):
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
            "ERROR", wx.ICON_ERROR|wx.OK)
        else:
            print('kk')
            folder, self.filename = os.path.split(path)
            self.st_info.SetLabel("  %s" % self.filename)
            # set the slider range min to max
            self.slider.SetRange(0, self.mc.Length())
            #self.mc.Play()

    def onPlay(self, evt):
        self.slider.SetRange(0, self.mc.Length())
        s1 = "  %s" % self.filename
        s2 = "  size: %s ms" % self.mc.Length()
        self.st_info.SetLabel(s1+s2)
        self.mc.Play()

    def onPause(self, evt):
        self.mc.Pause()

    def onStop(self, evt):
        self.mc.Stop()

    def onSeek(self, evt):
        """allows dragging the slider pointer to this position"""
        offset = self.slider.GetValue()
        self.mc.Seek(offset)

    def onTimer(self, evt):
        """moves the slider pointer"""
        offset = self.mc.Tell()
        self.slider.SetValue(offset)

def main():
    app = wx.App()
    frame = wx.Frame(None, -1, "play audio and video files", size = (500, 500))
    MediaPlayerPanel(frame, -1)
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()