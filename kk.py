import wx, wx.media

def playtimer(event):
    timer.Stop()
    mc.Play()

app = wx.App()
frame = wx.Frame(None, -1,size=(1910, 1070), pos=(0, 0))
mc = wx.media.MediaCtrl(frame)
if not mc.Load('「あぁ～！フロア熱狂の音ォ ！！」.mp4'):
    print('ff')
#mc.Play()
#mc.ShowPlayerControls()
timer = wx.Timer(frame)
frame.Bind(wx.EVT_TIMER, playtimer)
timer.Start(1000)
frame.Show()
app.MainLoop()