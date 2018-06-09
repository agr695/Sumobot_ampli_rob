#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import RPi.GPIO as GPIO

class servo():
    def __init__(self,pin,frec,dc_max,dc_min,dc_ini):
        self.pin=pin
        self.frec=frec
        self.dc_max=dc_max
        self.dc_min=dc_min
        self.rot_max=rot_max
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, frec)  # channel=12 frequency=50
        self.p.start(dc_ini)

    def set_new_pos(self,dc):
        if dc>self.dc_max
            self.p.ChangeDutyCycle(dc_max)
        elif dc<self.dc_min
            self.p.ChangeDutyCycle(dc_min)
        else
            self.p.ChangeDutyCycle(dc)
    def stop(self):
        self.p.stop()
        GPIO.cleanup()
