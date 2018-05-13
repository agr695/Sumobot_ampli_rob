#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from servo import servo as s

try:
    #inicialización servo
    pin = 12       #board
    frec = 50      #Hz
    dc_max = 10    #%
    dc_min = 2     #%
    rot_max = 180  #º
    p_ini = 0      #º
    a=s(pin,frec,dc_max,dc_min,rot_max, p_ini)

    cont=0
    while cont<180:
        a.set_new_pos(cont)
        cont=cont+5
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
a.stop()
