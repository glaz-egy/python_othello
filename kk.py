import wx, wx.media

app = wx.App()
frame = wx.Frame(None, -1)
mc = wx.media.MediaCtrl(frame)
if not mc.Load('「あぁ～！フロア熱狂の音ォ ！！」.mp4'):
    print('ff')
mc.Play()
mc.ShowPlayerControls()
frame.Show()
app.MainLoop()