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
while 1:
    try:
        if GPIO.input(fin_derecha)==1 or GPIO.input(fin_izquierda)==1:
            [izq,der]=m.modo_1(True)
        else:
            [izq,der]=m.modo_1(False)
        m_izq.set_dc(izq)
        m_der.set_dc(der)
        time.sleep(0.1)
    except KeyboardInterrupt:
        print "quit"
        GPIO.cleanup()
        break
