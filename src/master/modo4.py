#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import time
from libreria import modo
from libreria import servo
from libreria import imu

GPIO.setmode(GPIO.BOARD)   #Ponemos la placa en modo BOARD
GPIO_TRIGGER = 35          #Usamos el pin GPIO 25 como TRIGGER
GPIO_ECHO    = 37          #Usamos el pin GPIO 7 como ECHO
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  #Configuramos Trigger como salida
GPIO.setup(GPIO_ECHO,GPIO.IN)      #Configuramos Echo como entrada
GPIO.output(GPIO_TRIGGER,False)    #Ponemos el pin 25 como LOW


m=modo()

m_izq=servo(11,1000,60,0,0)
m_der=servo(13,1000,60,0,60)

conected=0
while conected==0:
    try:
        i=imu(1,0x68)  #tipo de bus, direccion i2c
        conected=1
    except IOError:
        print 'sensor no conectado'
        time.sleep(1)
    except KeyboardInterrupt:
        print "quit"
        GPIO.cleanup()
        break
cont=0
fin=0
flag = False
act = True
while 1:
    try:
        gyro_zout = imu.read_word_2c(0x47)
        a_x = i.read_word_2c(0x3b)
        a_y = i.read_word_2c(0x3d)
        a_z = i.read_word_2c(0x3f)
        accel_total=i.dist(a_x,a_y)
        if accel_total>2 and flag==0:
            ang=i.ang_golpe(a_x,a_y)
            flag = True
        else:
            cont+=1
            time.sleep(0.01)
            ang_girado = i.giro_z(gyro_zout)

        if ang<0:
            flag_giro = 0
        else:
            flag_giro = 1
        if ang - ang_girado > 0:
            flag_giro = 2


        if cont>=1000 and flag==False:

            if GPIO.input(fin_derecha)==1 or GPIO.input(fin_izquierda)==1:
                direct, act = m.modo_3(True, act)
            else:
                direct, act = m.modo_3(False, act)
        elif flag == True:
            if GPIO.input(fin_derecha)==1 or GPIO.input(fin_izquierda)==1:
                direct, act = m.modo_4(True, act)
            else:
                direct, act = m.modo_4(False, act)

        [izq,der] = direct

        m_izq.set_dc(izq)
        m_der.set_dc(der)
        time.sleep(0.2)
    except KeyboardInterrupt:
        print "quit"
        GPIO.cleanup()
        break
