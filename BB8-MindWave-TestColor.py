#!/usr/bin/env python

from __future__ import print_function
import time

from rcr.SpheroBB8 import SpheroBB8
from rcr.mindwave.MindWave import *

sphero = SpheroBB8.Sphero( 'FA:8B:91:F4:9D:22' )

mw = MindWave( "/dev/ttyUSB0", 1000, 0X0000 )
if( mw.connect() ):
    mwd = MindWaveData()
    sphero.setRGBLedOutput( 0, 0, 0 )
    last = 0
    t = time.time()
    while( time.time() - t < 60 ):
        mw.fillMindWaveData( mwd )
        attention = int( ( mwd.attentionESense * 255 )/100.0 )
        print( mwd.poorSignalQuality, mwd.attentionESense, attention )
        if( attention != last ):
            sphero.setRGBLedOutput( 0, attention, 0 )
            last = attention
        time.sleep( 0.001 )
    mw.disconnect()

sphero.close()
