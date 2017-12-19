import time
from lib import dronecore
from dronekit import connect

vehicle = connect('udp:192.168.1.177:14551', baud=57600, wait_ready=True)
#vehicle = connect('udp:10.42.0.1:14551', baud=57600, wait_ready=True)


dronecore.check_n_arm(vehicle)
dronecore.move_down(vehicle, 4) 
dronecore.take_off(vehicle)



#vehicle.mode = VehicleMode("LAND")
vehicle.close()

