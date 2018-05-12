#!/usr/bin/python

from mpu6050 import imu  as i
import time

conected=0
while conected==0:
    try:
        imu=i()
        conected=1
    except IOError:
        print 'sensor no conectado'
        time.sleep(1)

while 1:
    try:
        print "gyro data"
        print "---------"

        gyro_xout = imu.read_word_2c(0x43)
        gyro_yout = imu.read_word_2c(0x45)
        gyro_zout = imu.read_word_2c(0x47)

        print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
        print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
        print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)

        print
        print "accelerometer data"
        print "------------------"

        accel_xout = imu.read_word_2c(0x3b)
        accel_yout = imu.read_word_2c(0x3d)
        accel_zout = imu.read_word_2c(0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
        print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
        print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

        print "x rotation: " , imu.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        print "y rotation: " , imu.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        time.sleep(1)
    except KeyboardInterrupt:
        print 'parada manual'
        break
    except IOError:
        print 'sensor no conectado'
        time.sleep(1)
