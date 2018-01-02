import time
from dronecore import dronecore
from dronekit import connect

vehicle = connect('udp:192.168.1.177:14553', baud=57600, wait_ready=True)
#vehicle = connect('udp:10.42.0.1:14555', baud=57600, wait_ready=True)
#vehicle = connect('udp:127.0.0.1:14553', baud=57600, wait_ready=True)

dronecore.check_n_arm(vehicle)
dronecore.status_info(vehicle) 

######################
dronecore.take_off(vehicle, 2)

dronecore.move_forward(vehicle, 10)


#vehicle.mode = VehicleMode("LAND")
vehicle.close()

