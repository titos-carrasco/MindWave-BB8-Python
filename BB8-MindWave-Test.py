#!/usr/bin/env python

# BB-8 Python driver by Alistair Buxton <a.j.buxton@gmail.com>

from rcr.utils import Utils
from rcr.SpheroBB8 import SpheroBB8
from rcr.mindwave import MindWave

bb8 = SpheroBB8.Sphero( 'FA:8B:91:F4:9D:22' )

mw = MindWave.MindWave( "/dev/ttyUSB0", 1000, 0X00, 0X00 )
if( mw.connect() ):
    bb8.setRGBLedOutput( 0, 0, 0 )
    for i in range( 10000 ):
        mwd = mw.getMindWaveData()
        print vars(mwd)
        if( mwd.attentionESense >=90 ):
            bb8.setRGBLedOutput( 255, 0, 0 )
        elif( mwd.attentionESense >=70 ):
            bb8.setRGBLedOutput( 0, 255, 0 )
        elif( mwd.attentionESense >=50 ):
            bb8.setRGBLedOutput( 0, 0, 255 )
        #else:
        #    bb8.setRGBLedOutput( 0, 0, 0, 0, False )
        #bb8.ping()
        Utils.pause( 10 )
    mw.disconnect()

bb8.close()
