import time
from dronecore import dronecore
from dronekit import connect

#vehicle = connect('udp:192.168.1.177:14555', baud=57600, wait_ready=True)
vehicle = connect('udp:10.42.0.1:14555', baud=57600, wait_ready=True)

dronecore.check_n_arm(vehicle)
dronecore.status_info(vehicle) 

######################

dronecore.move_forward(vehicle, 10)
time.sleep(1)
dronecore.move_down(vehicle, 5)


#vehicle.mode = VehicleMode("LAND")
vehicle.close()

