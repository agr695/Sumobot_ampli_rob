#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import time
from libreria import modo
from libreria import servo
from libreria import imu

GPIO.setmode(GPIO.BOARD)
fin_derecha    = 40
fin_izquierda    = 38
GPIO.setup(fin_derecha,GPIO.IN)
GPIO.setup(fin_izquierda,GPIO.IN)

GPIO.setmode(GPIO.BOARD)   #Ponemos la placa en modo BOARD
GPIO_TRIGGER = 35          #Usamos el pin GPIO 25 como TRIGGER
GPIO_ECHO    = 37          #Usamos el pin GPIO 7 como ECHO
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  #Configuramos Trigger como salida
GPIO.setup(GPIO_ECHO,GPIO.IN)      #Configuramos Echo como entrada
GPIO.output(GPIO_TRIGGER,False)    #Ponemos el pin 25 como LOW

def mide_ld():
    GPIO.output(GPIO_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)
    start = time.time()
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()
    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()
    elapsed = stop-start
    distance = (elapsed * 34300)/2
    return distance

m=modo()

m_izq=servo(11,1000,60,0,0)
m_der=servo(13,1000,60,0,60)
i = 0
cam = True
while 1:
    try:
        d=mide_ld()
        if GPIO.input(fin_derecha)==1 or GPIO.input(fin_izquierda)==1:
            direct, act = m.party(cam, True, d, act)
        else:
            direct, act = m.party(cam, False, d, act)
        [izq,der] = direct

        m_izq.set_dc(izq)
        m_der.set_dc(der)
        time.sleep(0.2)
        if i < 20:
            i += 1
            cam = False
        else:
            i = 0
            cam = True

    except KeyboardInterrupt:
        print "quit"
        GPIO.cleanup()
        break
