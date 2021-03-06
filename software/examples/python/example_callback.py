#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change to your UID

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_dc import BrickDC

# Use velocity reached callback to swing back and forth between
# full speed forward and full speed backward
def cb_velocity_reached(velocity, dc):
    if velocity == 32767:
        print('Velocity: Full Speed forward, turning backward')
        dc.set_velocity(-32767)
    elif velocity == -32767:
        print('Velocity: Full Speed backward, turning forward')
        dc.set_velocity(32767)
    else:
        print('Error') # Can only happen if another program sets velocity

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    dc = BrickDC(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register "velocity reached callback" to cb_reached
    # cb_reached will be called every time a velocity set with
    # set_velocity is reached
    dc.register_callback(dc.CALLBACK_VELOCITY_REACHED,
                         lambda x: cb_velocity_reached(x, dc))

    dc.enable()
    # The acceleration has to be smaller or equal to the maximum acceleration
    # of the DC motor, otherwise cb_reached will be called too early
    dc.set_acceleration(5000) # Slow acceleration
    dc.set_velocity(32767) # Full speed forward

    raw_input('Press key to exit\n') # Use input() in Python 3
    dc.disable()
    ipcon.disconnect()
