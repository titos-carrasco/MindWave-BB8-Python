#!/usr/bin/env python

# BB-8 Python driver by Alistair Buxton <a.j.buxton@gmail.com>

from bluepy import btle

class BB8(btle.DefaultDelegate):
    def __init__(self, deviceAddress):
        btle.DefaultDelegate.__init__(self)

        # Address type must be "random" or it won't connect.
        self.peripheral = btle.Peripheral(deviceAddress, btle.ADDR_TYPE_RANDOM)
        self.peripheral.setDelegate(self)

        self.seq = 0

        # Attribute UUIDs are identical to Ollie.
        self.antidos = self.getSpheroCharacteristic('2bbd')
        self.wakecpu = self.getSpheroCharacteristic('2bbf')
        self.txpower = self.getSpheroCharacteristic('2bb2')
        self.roll = self.getSpheroCharacteristic('2ba1')
        self.notify = self.getSpheroCharacteristic('2ba6')

        # This startup sequence is also identical to the one for Ollie.
        # It even uses the same unlock code.
        print 'Sending antidos'
        self.antidos.write('011i3', withResponse=True)
        print 'Sending txpower'
        self.txpower.write('\x0007', withResponse=True)
        print 'Sending wakecpu'
        self.wakecpu.write('\x01', withResponse=True)

    def getSpheroCharacteristic(self, fragment):
        return self.peripheral.getCharacteristics(uuid='22bb746f'+fragment+'75542d6f726568705327')[0]

    def dumpCharacteristics(self):
        for s in self.peripheral.getServices():
            print s
            for c in s.getCharacteristics():
                print c, hex(c.handle)

    def cmd(self, did, cid, data=[], answer=True, resetTimeout=True):
        # Commands are as specified in Sphero API 1.50 PDF.
        # https://github.com/orbotix/DeveloperResources/
        seq = (self.seq&255)
        self.seq += 1
        sop2 = 0xfc
        sop2 |= 1 if answer else 0
        sop2 |= 2 if resetTimeout else 0
        dlen = len(data)+1
        chk = (sum(data)+did+cid+seq+dlen)&255
        chk ^= 255

        msg = [0xff, sop2, did, cid, seq, dlen] + data + [chk]
        print 'cmd:', ' '.join([chr(c).encode('hex') for c in msg])
        # Note: withResponse is very important. Most commands won't work without it.
        self.roll.write(''.join([chr(c) for c in msg]), withResponse=True)

    def handleNotification(self, cHandle, data):
        self.raw_data = data
        print 'Notification:', cHandle, data.encode('hex')

    def waitForNotifications(self, time):
        self.peripheral.waitForNotifications(time)

    def disconnect(self):
        self.peripheral.disconnect()

# This are mine (titos.carrasco@gmail.com)
# Documentation in https://sdk.sphero.com/

import threading

class Sphero( BB8 ):
    def __init__( self, deviceAddress ):
        self.mylock = threading.Lock()
        self.raw_data = {}

        BB8.__init__( self, deviceAddress )
        for i in range( 6 ):
            self.waitForNotifications( 0.5 )

    def lock( self ):
        self.mylock.acquire()

    def unlock( self ):
        self.mylock.release()

    def close( self ):
        try:
            self.lock()
            self.disconnect()
        except Exception as e:
            raise
        finally:
            self.unlock()

    def _parseResponseHeaders( self ):
        data = {
            'SOP1': ord( self.raw_data[0] ),
            'SOP2': ord( self.raw_data[1] ),
            'MRSP': ord( self.raw_data[2] ),
            'SEQ' : ord( self.raw_data[3] ),
            'DLEN': ord( self.raw_data[4] ),
            'CHK ': ord( self.raw_data[len( self.raw_data ) - 1] )
        }
        return data

    def ping( self ):
        try:
            self.lock()
            self.cmd( 0x00, 0x01 )
            self.waitForNotifications( 3.0 )
            data = self._parseResponseHeaders()
            print data
            return data
        except Exception as e:
            raise
        finally:
            self.unlock()

    def setHeading( self, degrees ):
        try:
            self.lock()
            self.cmd( 0x02, 0x01, [ (degrees >> 8) & 0xFF, degrees & 0xFF ] )
            self.waitForNotifications( 3.0 )
            data = self._parseResponseHeaders()
            print data
            return data
        except Exception as e:
            raise
        finally:
            self.unlock()

    def setRotationRate( self, rate ):
        try:
            self.lock()
            self.cmd( 0x02, 0x03, [ rate & 0xFF ] )
            self.waitForNotifications( 3.0 )
            data = self._parseResponseHeaders()
            print data
            return data
        except Exception as e:
            raise
        finally:
            self.unlock()

    def setRGBLedOutput( self, r, g, b ):
        try:
            self.lock()
            self.cmd( 0x02, 0x20, [ r & 0xFF, g & 0xFF, b &0xFF, 0x00 ] )
            self.waitForNotifications( 3.0 )
            data = self._parseResponseHeaders()
            print data
            return data
        except Exception as e:
            raise
        finally:
            self.unlock()

    def setBackLedOutput( self, bright ):
        try:
            self.lock()
            self.cmd( 0x02, 0x21, [ bright & 0xFF ] )
            self.waitForNotifications( 3.0 )
            data = self._parseResponseHeaders()
            print data
            return data
        except Exception as e:
            raise
        finally:
            self.unlock()

    def move( self, speed, degrees ):
        try:
            self.lock()
            if( speed <= 0 ): speed = 10;
            self.cmd( 0x02, 0x30, [ speed & 0xFF, (degrees >> 8) & 0xFF, degrees & 0xFF, 1 ] )
            self.waitForNotifications( 3.0 )
            data = self._parseResponseHeaders()
            print data
            return data
        except Exception as e:
            raise
        finally:
            self.unlock()

    def stop( self ):
        try:
            self.lock()
            self.cmd( 0x02, 0x30, [ 0, 0, 0, 0 ] )
            self.waitForNotifications( 3.0 )
            data = self._parseResponseHeaders()
            print data
            return data
        except Exception as e:
            raise
        finally:
            self.unlock()
