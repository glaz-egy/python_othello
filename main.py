# -*- coding:utf-8 -*-

import sys
import wx
import os

WhiteToBlack = {'white': (1, 'black', 0),
                'black': (0, 'white', 1)}

plusTuple = (-11, -10, -9, -1, 1, 9, 10, 11)

class Player:
    def __init__(self, color):
        self.Color = color
        self.GetPositon = []
        self.CanPut = self.SerchCanPut()
        self.TempGet = []
    
    def SerchCanPut(self):
        return 0

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
        player[0].GetPositon.append(44)
        player[0].GetPositon.append(55)
        self.Button[28].SetBackgroundColour('black')
        self.Button[35].SetBackgroundColour('black')
        player[1].GetPositon.append(45)
        player[1].GetPositon.append(54)

def ConversionField(num, FromField='OutRangeField'):
    if 'OutRangeField' == FromField:
        x = num//10 - 1
        return (num - (11 + (2 * x)))
    else:
        print('kk')

def ListinList(fromList, toList):
    for x in toList:
        fromList.append(x)

def IsGetCheck(color, pos):
    EnemyIs = WhiteToBlack[color][0]
    MyIs = WhiteToBlack[color][2]
    CanputFlag = False
    if pos not in player[0].GetPositon and pos not in player[1].GetPositon:
        for plus in plusTuple:
            if pos+plus in player[EnemyIs].GetPositon:
                GetBuffer = []
                for x in range(1, 9):
                    if pos+(plus*x) in field.FieldOut:
                        break
                    if pos+(plus*x) in player[MyIs].GetPositon:
                        CanputFlag = True
                        ListinList(player[MyIs].TempGet, GetBuffer)
                        break
                    GetBuffer.append(pos+(plus*x))
                else:
                    del GetBuffer
    return CanputFlag

def ChangeColor(color, pos):
    global nowColor
    EnemyIs = WhiteToBlack[color][0]
    MyIs = WhiteToBlack[color][2]
    player[MyIs].TempGet.append(pos)
    for num in player[MyIs].TempGet:
        if num in player[EnemyIs].GetPositon: player[EnemyIs].GetPositon.remove(num)
        player[MyIs].GetPositon.append(num)
        field.Button[ConversionField(num)].SetBackgroundColour(color)
    player[MyIs].TempGet = []
    nowColor = WhiteToBlack[color][1]

def ButtonPush(event):
    ID = event.GetId()
    if ID < 100:
        if IsGetCheck(nowColor, ID):
            ChangeColor(nowColor, ID)

if __name__=='__main__':
    app = wx.App()
    AppName = 'RFSP -Reversi of School Festival for Python-'
    frame = wx.Frame(None, -1, AppName, pos=(0, 0), size=(1200, 1000), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.MINIMIZE_BOX)
    panel = wx.Panel(frame, -1)
    player = [Player('white'), Player('black')]
    field = Field(panel, player)
    nowColor = 'black'
    frame.Bind(wx.EVT_BUTTON ,ButtonPush)
    frame.Show()
    app.MainLoop()