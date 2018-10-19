# -*- coding:utf-8 -*-

from copy import deepcopy
import numpy as np
import Relib
from time import sleep
import sys
import wx
import os

WhiteToBlack = {'white': (1, 'black', 0),
                'black': (0, 'white', 1)}

plusTuple = (-11, -10, -9, -1, 1, 9, 10, 11)

class ReversiBot:
    def __init__(self, color):
        self.Color = color
        self.Blank = [[0 for _ in range(8)] for _ in range(8)]
        self.Black = [[0 for _ in range(8)] for _ in range(8)]
        self.White = [[0 for _ in range(8)] for _ in range(8)]
        self.Network = Relib.Network.Network()

    def NextSet(self, blank):
        posList = []
        eva = []
        for x in blank:
            flag, players = IsGetCheck(self.Color, x, bot=True)
            if flag:
                posList.append(x)
                eva.append(self.EvaluationCalc(players, blank, x))
        if len(eva) == 0: return
        evaArray = np.array(eva)
        Next = posList[evaArray.argmax()]
        IsGetCheck(self.Color, Next)
        ChangeColor(self.Color, Next)

    def EvaluationCalc(self, players, blank, x):
        White = deepcopy(self.White)
        Black = deepcopy(self.Black)
        Blank = deepcopy(self.Blank)
        CopyPlayer = deepcopy(players)
        CopyBlank = deepcopy(blank)
        self.ChangeColor(CopyPlayer, CopyBlank, x)
        for x in CopyPlayer[0].GetPosition:
            White[x//10-1][x%10-1] = 1
        for x in CopyPlayer[1].GetPosition:
            Black[x//10-1][x%10-1] = 1
        for x in CopyBlank:
            Blank[x//10-1][x%10-1] = 1
        FieldData = np.array([White, Black, Blank])
        return self.Network.predict(FieldData.reshape(-1, 3, 8, 8))

    def ChangeColor(self, players, blank, pos):
        EnemyIs = WhiteToBlack[self.Color][0]
        MyIs = WhiteToBlack[self.Color][2]
        players[MyIs].TempGet.append(pos)
        for num in players[MyIs].TempGet:
            if num in players[EnemyIs].GetPosition: players[EnemyIs].GetPosition.remove(num)
            players[MyIs].GetPosition.append(num)
            if num in blank: blank.remove(num)
        players[MyIs].TempGet = []

class Player:
    def __init__(self, color):
        self.Color = color
        self.GetPosition = []
        self.TempGet = []

class Field:
    def __init__(self, panel, player):
        self.ButtonSize = 100
        self.Blanks = []
        self.FieldOut = []
        self.Button = []
        self.x, self.y = 8, 8
        layout = wx.GridSizer(rows=8, cols=8, gap=(0, 0))
        for i in range(self.y+2):
            for j in range(self.x+2):
                if i != 0 and j != 0 and i != self.x+1 and j != self.y+1:
                    self.Blanks.append(i*10+j)
                    self.Button.append(wx.Button(panel, i*10+j, ' '))
                    layout.Add(self.Button[-1], 0, wx.GROW)
                    self.Button[-1].SetBackgroundColour('#006F5F')
                else:
                    self.FieldOut.append(i*10+j)
        panel.SetSizer(layout)
        self.GameInit(player)

    def GameInit(self, player):
        self.Blanktimer = deepcopy(self.Blanks)
        self.Blank = deepcopy(self.Blanks)
        player[0].GetPosition = []
        player[1].GetPosition = []
        for x in self.Button:
            x.SetBackgroundColour('#006F5F')
        self.Button[27].SetBackgroundColour('white')
        self.Button[36].SetBackgroundColour('white')
        player[0].GetPosition.append(44)
        player[0].GetPosition.append(55)
        self.Blank.remove(44)
        self.Blank.remove(55)
        self.Button[28].SetBackgroundColour('black')
        self.Button[35].SetBackgroundColour('black')
        player[1].GetPosition.append(45)
        player[1].GetPosition.append(54)
        self.Blank.remove(45)
        self.Blank.remove(54)

def ConversionField(num, FromField='OutRangeField'):
    if 'OutRangeField' == FromField:
        x = -(11 + 2 *(num//10 - 1))
    else:
        x = 11 + 2*(num//8 - 1)
    return (num + x)


def IsGetCheck(color, pos, bot=False):
    if bot: pl = deepcopy(player)
    EnemyIs = WhiteToBlack[color][0]
    MyIs = WhiteToBlack[color][2]
    CanputFlag = False
    if pos not in player[0].GetPosition and pos not in player[1].GetPosition:
        for plus in plusTuple:
            if pos+plus in player[EnemyIs].GetPosition:
                GetBuffer = []
                for x in range(1, 9):
                    if pos+(plus*x) in field.FieldOut:
                        break
                    if pos+(plus*x) in player[MyIs].GetPosition:
                        CanputFlag = True
                        if not bot: player[MyIs].TempGet.extend(GetBuffer)
                        if bot : pl[MyIs].TempGet.extend(GetBuffer)
                        break
                    GetBuffer.append(pos+(plus*x))
                else:
                    del GetBuffer
    if not bot: return CanputFlag
    if bot: return (CanputFlag, pl)

def update(pos):
    if field.Blanktimer[-1] == player[0].GetPosition[-1]:
        field.Button[ConversionField(player[0].GetPosition[-1])].SetBackgroundColour('black')
        field.Button[ConversionField(player[1].GetPosition[-1])].SetBackgroundColour('white')
        player[0].GetPosition.insert(0, player[1].GetPosition[-1])
        player[1].GetPosition.insert(0, player[0].GetPosition[-1])
        player[0].GetPosition.remove(player[0].GetPosition[-1])
        player[1].GetPosition.remove(player[1].GetPosition[-1])
    field.Blanktimer.remove(field.Blanktimer[-1])
    print(field.Blanktimer[-1])
    if field.Blanktimer[-1] <= crossnum: timer.Stop()

def Endfunc():
    global crossnum
    player[0].GetPosition.sort()
    player[1].GetPosition.sort(reverse=True)
    crossnum1 = len(player[0].GetPosition)
    crossnum = ConversionField(crossnum1, FromField='InRangeField')
    timer.Start(50)
    for pos in field.Blanks:
        print(pos)
    print(player[0].GetPosition)

def ChangeColor(color, pos):
    global nowColor
    EnemyIs = WhiteToBlack[color][0]
    MyIs = WhiteToBlack[color][2]
    player[MyIs].TempGet.append(pos)
    for num in player[MyIs].TempGet:
        if num in player[EnemyIs].GetPosition: player[EnemyIs].GetPosition.remove(num)
        player[MyIs].GetPosition.append(num)
        if num in field.Blank: field.Blank.remove(num)
        field.Button[ConversionField(num)].SetBackgroundColour(color)
    player[MyIs].TempGet = []
    #nowColor = WhiteToBlack[color][1]

def Passfanc(Color):
    global nowColor
    nowColor = WhiteToBlack[Color][1]

def ButtonPush(event):
    global nowColor
    ID = event.GetId()
    if ID < 100:
        if IsGetCheck(nowColor, ID):
            ChangeColor(nowColor, ID)
            bot.NextSet(field.Blank)
            if len(field.Blank) == 0: Endfunc()
    if ID == 198:
        bot.NextSet(field.Blank)
        if len(field.Blank) == 0: Endfunc()
    if ID == 199:
        field.GameInit(player)
        nowColor = 'black'

if __name__=='__main__':
    app = wx.App()
    AppName = 'RSFP -Reversi of School Festival for Python-'
    frame = wx.Frame(None, -1, AppName, pos=(0, 0), size=(1200, 1000))
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    panel = wx.Panel(frame, -1)
    board = wx.Panel(panel, -1, size=(100, 100))
    Butzone = wx.Panel(panel, -1)
    player = [Player('white'), Player('black')]
    field = Field(board, player)
    bot = ReversiBot('white')
    nowColor = 'black'
    crossnum = 0
    timer = wx.Timer(frame)
    ButtonFont = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    PassButton = wx.Button(Butzone, 198, 'Pass')
    PassButton.SetFont(ButtonFont)
    ResetButton = wx.Button(Butzone, 199, 'Restart')
    ResetButton.SetFont(ButtonFont)
    sizer2 = wx.BoxSizer(wx.VERTICAL)
    sizer2.Add(PassButton, flag=wx.GROW | wx.RIGHT)
    sizer2.Add(ResetButton, flag=wx.GROW | wx.RIGHT)
    Butzone.SetSizer(sizer2)
    sizer.Add(board, 10, flag=wx.SHAPED)
    sizer.Add(Butzone, 1)
    panel.SetSizer(sizer)
    frame.Bind(wx.EVT_BUTTON ,ButtonPush)
    frame.Bind(wx.EVT_TIMER, update)
    frame.Show()
    app.MainLoop()