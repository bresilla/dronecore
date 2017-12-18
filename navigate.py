import time
import dronecore
import sensata
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

vehicle = connect('udp:192.168.1.177:14551', baud=57600, wait_ready=True)
#vehicle = connect('udp:10.42.0.1:14551', baud=57600, wait_ready=True)

while True:
    if sensata.analog(0) < 0.5:
        dronecore.move_left(vehicle)
        print "LEFT"
    elif sensata.analog(0) > 0.5:
        dronecore.move_right(vehicle)
        print "RIGHT"
    else:
        print "-----"
    time.sleep(1)

#vehicle.mode = VehicleMode("LAND")
vehicle.close()