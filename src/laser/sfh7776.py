#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smbus
import math
import time

class laser():
    def __init__(self,bus,address):
        self.bus = smbus.SMBus(bus) # or bus = smbus.SMBus(1) for Revision 2
        self.address = address
        # Power management value
        led_addr = 0x42
        ALS_addr = 0x41
        # Power management value
        set_led = 0x3F
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
