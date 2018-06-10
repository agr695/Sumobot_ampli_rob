#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import time
from libreria import modo
from libreria import servo

GPIO.setmode(GPIO.BOARD)
fin_derecha    = 40
fin_izquierda    = 38
GPIO.setup(fin_derecha,GPIO.IN)
GPIO.setup(fin_izquierda,GPIO.IN)

m=modo()
m_izq=servo(11,1000,60,0,0)
m_der=servo(13,1000,60,0,60)
act = True
while 1:
    try:
        if GPIO.input(fin_derecha)==1 or GPIO.input(fin_izquierda)==1:
            direct, act = m.modo_2(True, act)
        else:
            direct, act = m.modo_2(False, act)

        [izq,der] = direct
        m_izq.set_dc(izq)
        m_der.set_dc(der)
        time.sleep(0.1)
    except KeyboardInterrupt:
        print "quit"
        GPIO.cleanup()
        break
