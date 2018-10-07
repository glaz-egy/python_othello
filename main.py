# -*- coding:utf-8 -*-

import sys
import wx
import os

if __name__=='__main__':
    app = wx.App()
    AppName = 'OFSP -Othello of School Festival for Python-'
    frame = wx.Frame(None, -1, AppName, size=(800, 900), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.MINIMIZE_BOX)
    panel = wx.Panel(frame, -1)

    frame.Show()
    app.MainLoop()