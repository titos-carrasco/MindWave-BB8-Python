#!/usr/bin/python

import BB8_driver
from rcr.mindwave.MindWave import MindWave
from rcr.utils import Utils

bb8 = BB8_driver.Sphero( "BB-1104" )
bb8.deviceAddress = "C4:89:C2:7D:11:04"
bb8.connect()

bb8.start()
Utils.pause( 2000 )
bb8.set_rgb_led( 0, 0, 0, 0, False )

mw = MindWave( "/dev/ttyUSB0", 1000, 0xF6, 0x4F )
if( mw.connect() ):
    for i in range( 10000 ):
        mwd = mw.getMindWaveData()
        print "Signal:", mwd.poorSignalQuality, ", Attention eSense:", mwd.attentionESense
        if( mwd.attentionESense >=90 ):
            bb8.set_rgb_led( 255, 0, 0, 0, False )
        elif( mwd.attentionESense >=70 ):
            bb8.set_rgb_led( 0, 255, 0, 0, False )
        elif( mwd.attentionESense >=50 ):
            bb8.set_rgb_led( 0, 0, 255, 0, False )
        else:
            bb8.set_rgb_led( 0, 0, 0, 0, False )
        bb8.ping( False )
        Utils.pause( 10 )
    mw.disconnect()

bb8.join()
bb8.disconnect()
