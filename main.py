# -*- coding:utf-8 -*-

import sys
import wx
import os

class Player:
    def __init__(self, color):
        self.Color = color
        self.GetPositon = []
        self.CanPut = self.SerchCanput()
    
    def CanPut(self):

class Field:
    def __init__(self, panel, player):
        self.ButtonSize = 100
        self.FieldSize = []
        self.FieldOut = []
        self.Button = []
        self.x, self.y = 8, 8
        for i in range(self.x+2):
            for j in range(self.y+2):
                if i != 0 and j != 0 and i != self.x+1 and j != self.y+1:
                    self.FieldSize.append(i*10+j)
                    self.Button.append(wx.Button(panel, i*10+j, ' ',size=(self.ButtonSize, self.ButtonSize), pos=(self.ButtonSize*i, self.ButtonSize*j)))
                    self.Button[-1].SetBackgroundColour('#006F5F')
                else:
                    self.FieldOut.append(i*10+j)
        self.GameInit(player)

    def GameInit(self, player):
        self.Button[27].SetBackgroundColour('white')
        self.Button[36].SetBackgroundColour('white')
        player[0].GetPositon.append()
        self.Button[28].SetBackgroundColour('black')
        self.Button[35].SetBackgroundColour('black')
    

if __name__=='__main__':
    app = wx.App()
    AppName = 'RFSP -Reversi of School Festival for Python-'
    frame = wx.Frame(None, -1, AppName, pos=(0, 0), size=(1200, 1000), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.MINIMIZE_BOX)
    panel = wx.Panel(frame, -1)
    player = [Player('white'), Player('black')]
    field = Field(panel)
    frame.Show()
    app.MainLoop()