#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO_ECHO    = 40
GPIO.setup(GPIO_ECHO,GPIO.IN)

while 1:
    if GPIO.input(GPIO_ECHO)==1:
        print 'fin'
    else:
        print 'no fin'
    time.sleep(1)
