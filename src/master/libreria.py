#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smbus
import math
import time
import sys
import numpy as np
import random
import RPi.GPIO as GPIO

class imu():
    def __init__(self,bus,address):
        self.bus = smbus.SMBus(bus) # or bus = smbus.SMBus(1) for Revision 2
        self.address = address
        # Power management registers
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)
        self.giro = 0


    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self,adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self,a,b):
        return math.sqrt((a*a)+(b*b))

    def accel_total(self,a,b,c):
        return math.sqrt((a*a)+(b*b)+(c*c))

    def get_y_rotation(self,x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self,x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)

    def ang_golpe(self,x,y):
        return math.atan2(-x,y)

    def giro_z(self, gyro):
        self.gyro += gyro*0.01
        return(self.gyro)

class modo():

    def __init__(self):
        self.mov = {'avance': (100, (1, 0), 100 ,(1, 0)),
                    'retroceso': (100, (0, 1), 100, (0, 1)),
                    'giro_izq_a': (80, (1, 0), 100, (1, 0)),
                    'giro_dcha_a': (100, (1, 0), 80, (1, 0)),
                    'rota_izq': (0, (0, 1), 100, (1, 0)),
                    'rota_dcha': (100, (1, 0), 0, (0, 1)),
                    'giro_izq_r': (80, (0, 1), 100, (0, 1)),
                    'giro_dcha_r': (100, (0, 1), 80, (0, 1)),
                    'parado': (1, (0, 0), 1, (0, 0))}

        self.i_1 = 0
        self.mod_1 = True
        self.i_2 = 0
        self.mod_2 = 0
        self.k = 0
        self.partymode = 0

    def limite(self, ring):
        activa = False
        if ring == True and self.mod_1 == True:
            self.i_1 = random.randint(5, 10)
            ret = self.mov['rota_izq']
            self.mod_1 = False


        if self.i_1 == 0:
            ret = self.mov['avance']
            self.k += 1
            if self.k > 10:
                self.mod_1 = True
                self.k = 0
                activa = True
        else:
            ret = self.mov['rota_izq']
            self.i_1 -= 1

        return(ret, activa)

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

        return((ret[0],ret[2]))

    def modo_2(self, ring, activo):
        if activo == True:
            activo = True
            if self.mod_2 == True:
                self.i_2 += 1
                ret = self.mov['rota_dcha']
                if self.i_2 > 15:
                    self.mod_2 = False
            else:
                self.i_2 += 1
                ret = self.mov['rota_izq']
                if self.i_2 > 30:
                    self.mod_2 = True
                    self.i_2 = 0
            if ring == True:
                activo = False
        else:
            ret, activo = self.limite(ring)

        return((ret[0],ret[2]), activo)

    def modo_3(self, d, ring, activo):
        if activo == True:
            activo = True
            if d < 30:
                ret = self.mov['avance']
            else:
                ret = self.mov['rota_dcha']
            if ring == True:
                activo = False

        else:
            ret, activo = self.limite(ring)

        return((ret[0],ret[2]), activo)

    def modo_4(self, ring,  flag):
        if activo == True:
            activo = True

            if flag == 0:
                ret = self.mov['rota_izq']
            elif flag == 1:
                ret = self.mov['rota_dcha']
            elif flag == 2:
                ret = self.mov['avance']

            if ring == True:
                activo = False

        else:
            ret, activo = self.limite(ring)

        return((ret[0],ret[2]), activo)

    def party(self, cambio, ring, d, act):
        if cambio == True:
            self.partymode = random.randint(0, 3)

        if act == True:
            act = True
            if self.partymode == 0:
                ret, act = self.modo_1(ring)
            elif self.partymode == 1:
                ret, act = self.modo_2(ring, act)
            elif self.partymode == 2:
                ret, act = self.modo_3(d, ring, act)

            if ring == True:
                activo = False

        else:
            ret, act = self.limite(ring)

        return(ret, act)



class laser():
    def __init__(self,bus,address):
        self.bus = smbus.SMBus(bus) # or bus = smbus.SMBus(1) for Revision 2
        self.address = address
        # Power management value
        led_addr = 0x42
        ALS_addr = 0x41
        # Power management value
        set_led = 0x03
        act_ALS_PS = 0x06
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, led_addr, set_led)
        self.bus.write_byte_data(self.address, ALS_addr, act_ALS_PS)
        time.sleep(0.1)

    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self,adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

class servo():
    def __init__(self,pin,frec,dc_max,dc_min,dc_ini):
        self.pin=pin
        self.frec=frec
        self.dc_max=dc_max
        self.dc_min=dc_min
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, frec) 
        self.p.start(dc_ini)

    def set_dc(self,dc):
        if dc>self.dc_max:
            self.p.ChangeDutyCycle(self.dc_max)
        elif dc<self.dc_min:
            self.p.ChangeDutyCycle(self.dc_min)
        else:
            self.p.ChangeDutyCycle(dc)
    def stop(self):
        self.p.stop()
        GPIO.cleanup()
