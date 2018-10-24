# -*- coding:utf-8 -*-

from datetime import datetime
import Relib

type_dic = {Relib.GAME_LOG:'[Game Log] ',\
            Relib.SYSTEM_LOG:'[System Log] ',\
            Relib.FILE_LOG:'[File Log] ',\
            Relib.ERROR:'[Error] ',\
            Relib.DEBAG:'[Debag] ',\
            Relib.LEARN:'[Learn log] '}

class LogControl:
    def __init__(self, file_name):
        self.name = file_name

    def LogWrite(self, write_text, logtype=Relib.GAME_LOG, write_type='a'):
        with open(self.name, write_type) as f:
            f.write(datetime.now().strftime("[%Y/%m/%d %H:%M:%S] ")+type_dic[logtype]+write_text+'\n')
