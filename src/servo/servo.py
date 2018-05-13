#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import RPi.GPIO as GPIO

class servo():
    def __init__(self,pin,frec,dc_max,dc_min,rot_max,p_ini):
        self.pin=pin
        self.frec=frec
        self.dc_max=dc_max
        self.dc_min=dc_min
        self.rot_max=rot_max
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, frec)  # channel=12 frequency=50
        self.p.start(self.dc_min+(self.dc_max-self.dc_min)*(float(p_ini)/self.rot_max))

    def set_new_pos(self,pos):
        self.p.ChangeDutyCycle(self.dc_min+(self.dc_max-self.dc_min)*(float(pos)/self.rot_max))

    def stop(self):
        self.p.stop()
        GPIO.cleanup()
