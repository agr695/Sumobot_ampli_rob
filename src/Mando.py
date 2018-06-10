from __future__ import print_function
from inputs import get_gamepad
import multiprocessing
import os
import signal
import time
import sys
import numpy as np
import math
import random
#import Visualize

def model(): # Esto sera lo que de el modelo de la red
    model = 1
    return(model)

class mando():

    def __init__(self):
        self.vel = 0
        self.dif_vel = 20
        self.tipo = 0
        self.out = [0, 0]
        self.ang_g = 0
        self.ang_l = 0
        self.ang_b = [-40, 40]
        self.ang_obj = []
##        self.mov = {'avance': (100, 100), 'retroceso': (-100, -100), 'agiro_i': (80, 100), 'agiro_d': (100, 80),
##                    'sgiro_i': (-100, 100), 'sgiro_d': (100, -100), 'rgiro_i': (-80, -100), 'rgiro_i': (-100, -80)}

        self.mov = {'avance': (100, (1, 0), 100 ,(1, 0)),
                    'retroceso': (100, (0, 1), 100, (0, 1)),
                    'giro_izq_a': (80, (1, 0), 100, (1, 0)),
                    'giro_dcha_a': (100, (1, 0), 80, (1, 0)),
                    'rota_izq': (100, (0, 1), 100, (1, 0)),
                    'rota_dcha': (100, (1, 0), 100, (0, 1)),
                    'giro_izq_r': (80, (0, 1), 100, (0, 1)),
                    'giro_dcha_r': (100, (0, 1), 80, (0, 1)),
                    'parado': (1, (0, 0), 1, (0, 0))}
##        self.mov = {'avance': (100, (1, 0), 100 ,(1, 0)),
##                    'retroceso': (100, (0, 1), 100, (0, 1)),
##                    'giro_izq_a': (80, (1, 0), 100, (1, 0)),
##                    'giro_dcha_a': (100, (1, 0), 80, (1, 0)),
##                    'rota_izq': (100, (0, 1), 100, (1, 0)),
##                    'rota_dcha': (100, (1, 0), 100, (0, 1)),
##                    'giro_izq_r': (80, (0, 1), 100, (0, 1)),
##                    'giro_dcha_r': (100, (0, 1), 80, (0, 1)),
##                    'parado': (1, (0, 0), 1, (0, 0))}

        self.i_1 = 0
        self.mod_1 = True
        self.i_2 = 0
        self.mod_2 = 0
    
    def botones(self, st, est):
        vec = [False, False, False, False, False, False, False, False]
        if est == 1:
            if '825' == st:
                vec[0] = True
            if '826' == st:
                vec[1] = True
            if '827' == st:
                vec[2] = True
            if '828' == st:
                vec[3] = True
            if '829' == st:
                vec[4] = True
            if '831' == st:
                vec[5] = True
            if '833' == st:
                vec[6] = True
            if '834' == st:
                vec[7] = True

        return(vec)

    def flechas(self, st, est):
        vec = [False, False, False, False]
        if 'ABS_X' in est:
            if st == '0':
                vec[0] = True
            elif st == '255':
                vec[1] = True
            elif st == '127':
                vec[0] = False
                vec[1] = False

        elif 'ABS_Y' in est:
            if st == '0':
                vec[2] = True
            elif st == '255':
                vec[3] = True
            elif st == '127':
                vec[2] = False
                vec[3] = False

        return(vec)

    def fusion_mando(self, valor, estado, valor2, estado2):
        v1 = self.botones(valor, estado)
        v2 = self.flechas(valor2, estado2)
        
        self.v = v1 + v2
        
        return(self.v)

    def movimientos(self):
        ret = self.mov['parado']
        
        if self.v[10] == True:
            ret = self.mov['avance']

        if self.v[11] == True:
            ret = self.mov['retroceso']

        if self.v[4] == True:
            ret = self.mov['rota_izq']

        if self.v[5] == True:
            ret = self.mov['rota_dcha']

        if self.v[8] == True:
            ret = self.mov['giro_izq_a']

        if self.v[9] == True:
            ret = self.mov['giro_dcha_a']
            
        print(ret)
        
        return(ret)

    def modo_1(self, ring):
        if ring == True and self.mod_1 == True:
            self.i_1 = random.randint(5, 10)
            ret = self.mov['rota_izq']
            self.mod_1 = False

        if self.i_1 == 0:
            ret = self.mov['avance']
            self.mod_1 = True
        else:
            ret = self.mov['rota_izq']
            self.i_1 -= 1

        return(ret)

    def modo_2(self):
        if self.mod_2 == True:
            self.i_2 += 1
            ret = self.mov['rota_dcha']
            if self.i_2 > 15:
                self.mod_2 = False

            print('hey')
        else:
            self.i_2 += 1
            ret = self.mov['rota_izq']
            if self.i_2 > 30:
                self.mod_2 = True
                self.i_2 = 0
            print('hoe')
        return(ret)

    def modo_3(self, d):
        if d < 30:
            ret = self.mov['avance']
        else:
            ret = self.mov['rota_dcha']

        return(ret)

    def objetivo(self, model):
        d = model.fit(self.medidas)

        detect = False
        if int(round(d[1])) == 1:
            detect = True
            self.obj = math.ceil((self.medidas/2))
                    
        return(detect, self.obj)

    def rellena(self, m, f):
        # Hay que vaciarlo cada vez que se diga
        if f == True:
            self.medidas = []
        p = 5

        self.medidas.append(m)

        flag = False
        if len(self.medidas) == p:
            flag = True

        return(self.medidas, flag)
        
    def ang_act(self, meas, p, i):
        ang = (meas[1] - meas[0])*i/p + meas[0]
        ang_l = ang + 40 - self.ang_g
        
        if ang_l < -40:
            ang_l = -40
        if ang_l > 40:
            ang_l = 40
            
        return(ang_l)

    def ang_meas(self):
        return((self.obj-20, self.obj+20))
                
    def datos(self):
        pass

    def main(self):
        #model = model()
        h = 0
        Flag = True
        estado = 0
        estado2 = 0
        valor = '12'
        flecha = '000'
        #signal.signal(signal.SIGINT, signal_handler)
        while True:
            events = get_gamepad()
            for event in events:
                if 'Key' in str(event.ev_type):
                    Flag = True
                elif 'Absolute' in str(event.ev_type):
                    Flag = False

                h += 1
                if h == 1:
                    valor = str(event.state)
                    valor = valor[3:6]
                    flecha = '000'
                    cod = 'asdf'
                    if Flag == False:
                        flecha = str(event.state)
                        cod = str(event.code)

                elif h == 2:
                    estado = event.state
                    if Flag == False:
                        h = 0

                elif h == 3:
                    h = 0


            v = self.fusion_mando(valor, estado, flecha, cod)
            ## [X, A, B, Y, L1, R1, Sel, Start, l, r, u, d]
            
            if v[0] == True:
                ret = self.modo_1(True)
            elif v[3] == True:
                ret = self.modo_2()
            elif v[1] == True:
                ret = self.modo_3(30)
            else:
                ret = self.movimientos()

            print(ret)


a = mando()
a.main()
