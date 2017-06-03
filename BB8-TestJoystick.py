#!/usr/bin/env python

from __future__ import print_function
import time
import pygame

from rcr.SpheroBB8 import SpheroBB8

def main():
    sphero = SpheroBB8.Sphero( 'FA:8B:91:F4:9D:22' )
    response = sphero.ping()
    response = sphero.setHeading( 0 )
    speed = 50

    pygame.init()
    joystick = pygame.joystick.Joystick( 0 )
    joystick.init()
    axes = [0]*joystick.get_numaxes()
    ( _x, _y ) = ( 0, 0 )
    running = True
    while( running ):
        try:
            events = pygame.event.get()
            for event in events:
                if( event.type == pygame.JOYBUTTONDOWN ):
                    if( event.button == 7 ):
                        running = False
                elif( event.type == pygame.JOYAXISMOTION and event.joy == 0 ):
                    axes[event.axis] = int( round( event.value, 0 ) )

            ( x, y ) = ( axes[0], -axes[1] )
            if( ( _x, _y )!=( x, y ) ):
                (_x, _y) = (x, y)
                if(x==0 and y==1):
                    print( "Up" )
                    response = sphero.move( speed, 0 )
                elif(x==0 and y==-1):
                    print( "Down" )
                    response = sphero.move( speed, 180 )
                elif(x==-1 and y==0):
                    print( "Left" )
                    response = sphero.move( speed, 270 )
                elif(x==1 and y==0):
                    print( "Right" )
                    response = sphero.move( speed, 90 )
                elif(x==-1 and y==1):
                    print( "UpLeft" )
                elif(x==1 and y==1):
                    print( "UpRight" )
                elif(x==-1 and y==-1):
                    print( "DownLeft" )
                elif(x==1 and y==-1):
                    print( "DownRight" )
                else:
                    print( "Stop" )
                    response = sphero.stop()
            time.sleep( 0.1 )
        except Exception as e:
            print( e )
            break
    pygame.quit()
    sphero.stop()
    sphero.close()

main()

"""
# Test
response = sphero.setRotationRate( 0xC8 )
response = sphero.setRGBLedOutput( 0xFF, 0xFF, 0x00 )
response = sphero.setBackLedOutput( 0xFF )

time.sleep( 4 );

response = sphero.move( 40, 180 )
time.sleep( 4 );

sphero.close()
"""
