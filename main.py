# -*- coding:utf-8 -*-

from copy import deepcopy
import numpy as np
import Relib
from time import sleep
import wx.media
import sys
import wx
import os

NumberRank = ['01st', '02nd', '03rd', '04th', '05th', '06th', '07th', '08th', '09th', '10th']

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
        self.Network.load_params('gene/params100.pkl')
        log.LogWrite('Init ReversiBot')

    def NextSet(self, blank):
        global passFlag
        global nowColor
        global Flag
        posList = []
        eva = []
        for x in blank:
            flag, players = IsGetCheck(self.Color, x, bot=True)
            if flag:
                posList.append(x)
                eva.append(self.EvaluationCalc(players, blank, x))
                print('Position: {}, Eva: {}'.format(posList[-1], eva[-1]))
        if len(eva) == 0 and passFlag:
            Endfunc()
        elif len(eva) == 0:
            MsDialog = wx.MessageDialog(frame, 'AIはパスした。あなたはどうする？', 'あっれれ～？　相手が動いていないよ～？')
            MsDialog.ShowModal()
            MsDialog.Destroy()
            Flag = not Flag
            nowColor = 'black'
            log.LogWrite('AI is pass')
            return
        passFlag = False
        evaArray = np.array(eva)
        Next = posList[evaArray.argmax()]
        print('Best pos: {}, Best Eva: {}'.format(Next, evaArray[evaArray.argmax()]))
        log.LogWrite('Best pos: {}, Best Eva: {}'.format(Next, evaArray[evaArray.argmax()]))
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
        global nowColor
        global passFlag
        log.LogWrite('Init field')
        passFlag = False
        nowColor = 'black'
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

class MusicPlay:
    def __init__(self):
        self.frame = wx.Frame(None, -1, title='「あぁ～！フロア熱狂の音ォ ！！」', size=(1910, 1070), pos=(0, 0), style=wx.CAPTION | wx.MAXIMIZE |wx.STAY_ON_TOP)
        self.MusicContrl = wx.media.MediaCtrl(self.frame)
        self.MusicContrl.Load('「あぁ～！フロア熱狂の音ォ ！！」.mp4')
        self.frame.Show()
        self.PlayTimer = wx.Timer(self.frame, 2018)
        self.EndTimer = wx.Timer(self.frame, 2019)
        self.frame.Bind(wx.EVT_TIMER, self.Timer)

    def Start(self):
        self.PlayTimer.Start(1000)

    def Timer(self, event):
        if event.GetId() == 2018:
            self.Play()
        if event.GetId() == 2019 and self.MusicContrl.GetState() != wx.media.MEDIASTATE_PLAYING:
            self.End()

    def Play(self):
        self.PlayTimer.Stop()
        self.MusicContrl.Play()
        self.EndTimer.Start(100)
    
    def End(self):
        self.EndTimer.Stop()
        self.frame.Destroy()
        self.MusicContrl.Destroy()


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
                    if pos+(plus*x) in field.Blank:
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

def Swap(lists, fromData, toData):
    lists[fromData], lists[toData] = lists[toData], lists[fromData]
    return lists

def IsUpdateRanking():
    global RankList
    x = 9
    Score = (len(player[1].GetPosition) - len(player[0].GetPosition)) if len(player[0].GetPosition) != 0 else 64
    if Score > (int(RankList[9][0]) if RankList[9][0] != 'N/A' else 0):
        NameDialog = wx.TextEntryDialog(None, '君、リバーシ強いね。ってか名前教えて。', '君の名前を教えて欲しいな')
        NameDialog.SetValue('ここに名前を入力してね')
        if NameDialog.ShowModal() == wx.ID_OK:
            Name = NameDialog.GetValue()
            NameDialog.Destroy()
            print(Name)
            while (Score > (int(RankList[x-1][0]) if RankList[x-1][0] != 'N/A' else 0)) and x != 0:
                x -= 1
            RankList.insert(x, [Score, Name])
            RankList = RankList[:10]
            with open('Ranking.txt', 'w') as f:
                for rank in RankList:
                    f.write('{}-{}\n'.format(rank[0], rank[1]))
            LoadRanking()
    if Score == 64:
        log.LogWrite('Fill all black')
        media = MusicPlay()
        media.Start()

def update(event):
    global nowColor
    global Flag
    global sleeps
    if event.GetId() == 195:
        sleeps += 1
        if sleeps == 10:
            TurnTimer.Stop()
            sleeps = 0
            bot.NextSet(field.Blank)
    if event.GetId() == 196:
        Flag = False
        if len(player[0].GetPosition) == 0 or len(player[1].GetPosition) == 0:
            timer.Stop()
            IsUpdateRanking()
            return
        if field.Blanktimer[-1] == player[0].GetPosition[-1]:
            field.Button[ConversionField(player[0].GetPosition[-1])].SetBackgroundColour('black')
            field.Button[ConversionField(player[1].GetPosition[-1])].SetBackgroundColour('white')
            player[0].GetPosition.insert(0, player[1].GetPosition[-1])
            player[1].GetPosition.insert(0, player[0].GetPosition[-1])
            player[0].GetPosition.remove(player[0].GetPosition[-1])
            player[1].GetPosition.remove(player[1].GetPosition[-1])
        field.Blanktimer.remove(field.Blanktimer[-1])
        if field.Blanktimer[-1] < crossnum:
            timer.Stop()
            IsUpdateRanking()
    elif event.GetId() == 197:
        EnemyIs = WhiteToBlack[nowColor][0]
        MyIs = WhiteToBlack[nowColor][2]
        num = player[MyIs].TempGet[-1]
        if num in player[EnemyIs].GetPosition: player[EnemyIs].GetPosition.remove(num)
        if num in field.Blank: field.Blank.remove(num)
        player[MyIs].GetPosition.append(num)
        field.Button[ConversionField(num)].SetBackgroundColour(nowColor)
        player[MyIs].TempGet.remove(num)
        if len(player[MyIs].TempGet) == 0:
            ChangeColorTimer.Stop()
            player[MyIs].TempGet = []
            nowColor = WhiteToBlack[nowColor][1]
            Flag = not Flag
            if len(field.Blank) == 0: Endfunc()
            elif Flag:
                TurnTimer.Start(50)
            

def Endfunc():
    global crossnum
    player[0].GetPosition.sort()
    player[1].GetPosition.sort(reverse=True)
    crossnum1 = len(player[1].GetPosition)
    crossnum = ConversionField(crossnum1, FromField='InRangeField')
    #timer.Start(30)

def ChangeColor(color, pos):
    global nowColor
    MyIs = WhiteToBlack[nowColor][2]
    player[MyIs].TempGet.reverse()
    player[MyIs].TempGet.append(pos)
    ChangeColorTimer.Start(80)

def Passfanc(Color):
    global nowColor
    nowColor = WhiteToBlack[Color][1]

def ButtonPush(event):
    global nowColor
    global Flag
    global passFlag
    print(nowColor)
    ID = event.GetId()
    if not ChangeColorTimer.IsRunning():
        if ID < 100:
            if IsGetCheck(nowColor, ID):
                log.LogWrite('Player next {}'.format(ID))
                ChangeColor(nowColor, ID)
        if ID == 198:
            passFlag = True
            Flag = not Flag
            nowColor = WhiteToBlack[nowColor][1]
            bot.NextSet(field.Blank)
            if len(field.Blank) == 0: Endfunc()
        if ID == 199:
            timer.Stop()
            ChangeColorTimer.Stop()
            TurnTimer.Stop()
            field.GameInit(player)

def SetRanking(sizer):
    rank = []
    font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    size = wx.BoxSizer(wx.VERTICAL)
    for x in range(10):
        rank.append(wx.StaticText(Butzone, -1, ' '))
        rank[-1].SetFont(font)
        sizer.Add(rank[-1], flag=wx.GROW | wx.LIGHT | wx.ALIGN_BOTTOM)
    return rank

def LoadRanking():
    global Ranking
    fline = []
    with open('Ranking.txt', 'r') as f:
        for ftemp in f:
            Point, Name = ftemp.split('-')
            Name = Name.replace('\n', '')
            fline.append([Point, Name])
    for rank in range(len(Ranking)):
        Ranking[rank].SetLabel('{} : {}\n得点 : {}'.format(NumberRank[rank], fline[rank][1], fline[rank][0]))
    log.LogWrite('Update Ranking')
    return fline
    

if __name__=='__main__':
    app = wx.App()
    log = Relib.SystemControl.LogControl('game.log')
    AppName = 'RSFP -Reversi of School Festival for Python-'
    frame = wx.Frame(None, -1, AppName, pos=(0, 0), size=(1500, 1000))
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    panel = wx.Panel(frame, -1)
    board = wx.Panel(panel, -1, size=(100, 100))
    Butzone = wx.Panel(panel, -1, size=(600, 1000))
    player = [Player('white'), Player('black')]
    field = Field(board, player)
    bot = ReversiBot('white')
    nowColor = 'black'
    crossnum = 0
    sleeps = 0
    passFlag = False
    Flag = False
    TurnTimer = wx.Timer(frame, id=195)
    timer = wx.Timer(frame, id=196)
    ChangeColorTimer = wx.Timer(frame, id=197)
    ButtonFont = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    PassButton = wx.Button(Butzone, 198, 'Pass')
    PassButton.SetFont(ButtonFont)
    ResetButton = wx.Button(Butzone, 199, 'Restart')
    ResetButton.SetFont(ButtonFont)
    sizer2 = wx.BoxSizer(wx.VERTICAL)
    sizer2.Add(PassButton, flag=wx.GROW | wx.RIGHT)
    sizer2.Add(ResetButton, flag=wx.GROW | wx.RIGHT)
    Ranking = SetRanking(sizer2)
    RankList = LoadRanking()
    Butzone.SetSizer(sizer2)
    sizer.Add(board, 10, flag=wx.SHAPED)
    sizer.Add(Butzone, 1)
    panel.SetSizer(sizer)
    frame.Bind(wx.EVT_BUTTON ,ButtonPush)
    frame.Bind(wx.EVT_TIMER, update)
    frame.Show()
    app.MainLoop()