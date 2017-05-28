#!/usr/bin/env python

# BB-8 Python driver by Alistair Buxton <a.j.buxton@gmail.com>

from rcr.utils import Utils
from rcr.SpheroBB8 import SpheroBB8

sphero = SpheroBB8.Sphero( 'FA:8B:91:F4:9D:22' )

# Test
response = sphero.ping()
response = sphero.setHeading( 0 )
response = sphero.setRotationRate( 0xC8 )
response = sphero.setRGBLedOutput( 0xFF, 0xFF, 0x00 )
response = sphero.setBackLedOutput( 0xFF )

response = sphero.move( 40, 0 )
Utils.pause( 4000 );
response = sphero.move( 40, 180 )
Utils.pause( 4000 );

response = sphero.stop()
sphero.close()
