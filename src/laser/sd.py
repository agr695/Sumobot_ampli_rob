import time
from sfh7776 import laser  as laser

conected=0
while conected==0:
    try:
        imu=laser(1,0x39)  #tipo de bus, direccion i2c
        conected=1
    except IOError:
        print 'sensor no conectado'
        time.sleep(1)
        except KeyboardInterrupt:
            print 'parada manual'
            break
while 1:
    try:
        proximity=read_word(0x44)
        VIS=read_word(0x46)
        IR=read_word(0x48)

        print proximity
        print
        print VIS
        print
        print IR

    except KeyboardInterrupt:
        print 'parada manual'
        break
    except IOError:
        print 'sensor no conectado'
        time.sleep(1)
