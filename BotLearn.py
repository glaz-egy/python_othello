# -*- coding:utf-8 -*-

from joblib import Parallel, delayed
from copy import deepcopy
import numpy as np
import Relib
import sys
import os

WhiteToBlack = {'white': (1, 'black', 0),
                'black': (0, 'white', 1)}

plusTuple = (-11, -10, -9, -1, 1, 9, 10, 11)

class ReversiBot:
    def __init__(self, color, params):
        self.Color = color
        self.Blank = [[0 for _ in range(8)] for _ in range(8)]
        self.Black = [[0 for _ in range(8)] for _ in range(8)]
        self.White = [[0 for _ in range(8)] for _ in range(8)]
        self.Network = Relib.Network.Network()
        self.Network.load_params(file_name=params)

    def NextSet(self, blank, player, field):
        posList = []
        eva = []
        for x in blank:
            flag, players = IsGetCheck(self.Color, x, player, field, bot=True)
            if flag:
                posList.append(x)
                eva.append(self.EvaluationCalc(players, blank, x))
        if len(eva) == 0:
            return
        evaArray = np.array(eva)
        Next = posList[evaArray.argmax()]
        IsGetCheck(self.Color, Next, player, field)
        ChangeColor(self.Color, Next, player, field)

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
    def __init__(self, player):
        self.ButtonSize = 100
        self.Blanks = []
        self.FieldOut = []
        self.x, self.y = 8, 8
        for i in range(self.y+2):
            for j in range(self.x+2):
                if i != 0 and j != 0 and i != self.x+1 and j != self.y+1:
                    self.Blanks.append(i*10+j)
                else:
                    self.FieldOut.append(i*10+j)
        self.GameInit(player)

    def GameInit(self, player):
        self.Blanktimer = deepcopy(self.Blanks)
        self.Blank = deepcopy(self.Blanks)
        player[0].GetPosition = []
        player[1].GetPosition = []
        player[0].GetPosition.append(44)
        player[0].GetPosition.append(55)
        self.Blank.remove(44)
        self.Blank.remove(55)
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


def IsGetCheck(color, pos, player, field, bot=False):
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

def Endfunc(player):
    score = len(player[0].GetPosition) - len(player[1].GetPosition)
    print('       {}'.format(score))
    return (False, score)

def ChangeColor(color, pos, player, field):
    MyIs = WhiteToBlack[color][2]
    EnemyIs = WhiteToBlack[color][0]
    player[MyIs].TempGet.append(pos)
    for num in player[MyIs].TempGet:
        if num in player[EnemyIs].GetPosition: player[EnemyIs].GetPosition.remove(num)
        if num in field.Blank: field.Blank.remove(num)
        player[MyIs].GetPosition.append(num)
    player[MyIs].TempGet = []


def Learn(params):
    player = deepcopy(playerSeed)
    field = Field(player)
    bot1 = ReversiBot('black', params='gene/params100.pkl')
    bot2 = ReversiBot('white', params=params)
    NoendFlag = True
    temp1 = []
    temp2 = []
    while NoendFlag:
        bot1.NextSet(field.Blank, player, field)
        bot2.NextSet(field.Blank, player, field)
        if len(field.Blank) == 0 or (temp1 == player[0].GetPosition and temp2 == player[1].GetPosition):
            NoendFlag, score = Endfunc(player)
        temp1 = player[0].GetPosition[:]
        temp2 = player[1].GetPosition[:]
    return [bot2.Network.params, score]

if __name__=='__main__':
    playerSeed = [Player('white'), Player('black')]
    genes = 50
    paramsnum = 100
    Evo = Relib.Evolutionary.GeneManagement()
    if not os.path.isfile('gene/params0.pkl'):
        Evo.CreateGene()
    for i in range(genes):
        paramsScore = []
        print(i)
        paramsScore += Parallel(n_jobs=-1)([delayed(Learn)('gene/params{}.pkl'.format(n)) for n in range(paramsnum)])
        #paramsScore += Learn('gene/params{}.pkl'.format(j))
        Evo.SelectGene(paramsScore)