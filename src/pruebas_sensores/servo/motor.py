#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from servo import servo as s

try:
    #inicialización servo
    pin = 12       #board
    frec = 1000      #Hz
    dc_max = 60   #%
    dc_min = 0     #%
    p_ini = 0      #º
    a=s(pin,frec,dc_max,dc_min, p_ini)

    cont=0
    while cont<60:
        a.set_dc(cont)
        cont=cont+1
        time.sleep(0.25)
except KeyboardInterrupt:
    pass
a.stop()
