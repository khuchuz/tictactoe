import os
import json
import base64
from glob import glob
import shelve

#asumsi, hanya ada player X dan O
class PlayerServerInterface:
    def __init__(self):
        self.playersX = [0,1]
        self.playersO = [3,4]
        self.last_turn = 'X'

    def get_last_turn(self,params=[]):
        try:
            return dict(status='OK',last_turn=self.last_turn)
        except:
            return dict(status='ERROR')

    def set_location(self,params=[]):
        pnum = params[0]
        lokasi = params[1]
        try:
            lokasi = json.loads(lokasi)
            if pnum == 'x':
                self.playersX = lokasi
                self.last_turn = 'O'
            if pnum == 'o':
                self.playersO = lokasi
                self.last_turn = 'X'
            return dict(status='OK')
        except:
            return dict(status='ERROR')

    def get_location(self,params=[]):
        try:
            return dict(status='OK',location=[self.playersX,self.playersO])
        except:
            return dict(status='ERROR')

    def reset(self,params=[]):
        try:
            self.playersX = []
            self.playersO = []
            self.last_turn = 'X'
            return dict(status='OK')
        except:
            return dict(status='ERROR')



if __name__=='__main__':
    p = PlayerServerInterface()
    p.set_location(['x',[]])
    p.set_location(['o',[5,7,8]])
    print(p.get_last_turn())
    print(p.get_location())
