import time
from dronecore import dronecore
from dronekit import connect, VehicleMode

vehicle = connect('udp:192.168.1.177:14555', baud=57600, wait_ready=True)
#vehicle = connect('udp:10.42.0.1:14555', baud=57600, wait_ready=True)
#vehicle = connect('udp:127.0.0.1:14553', baud=57600, wait_ready=True)

dronecore.check_n_arm(vehicle)
dronecore.status_info(vehicle) 

######################
vehicle.airspeed = 3

altittude = 1
waypoints = [(44.549095,   11.416070, altittude),
            (44.549980,	11.416741, altittude), 
            (44.549969,	11.416780, altittude), 
            (44.549084,	11.416105, altittude),
            (44.549068,	11.416142, altittude),
            (44.549953,	11.416820, altittude),
            (44.549938,	11.416853, altittude),
            (44.549053,	11.416171, altittude),
            (44.549038,	11.416210, altittude),
            (44.549923,	11.416887, altittude), 
            (44.549908,	11.416924, altittude),
            (44.549023,	11.416246, altittude),
            (44.549004,	11.416280, altittude),
            (44.549900,	11.416959, altittude),
            (44.549885,	11.416998, altittude),
            (44.548988,	11.416317, altittude),
            (44.548977,	11.416351, altittude),
            (44.549870,	11.417032, altittude),
            (44.549854,	11.417070, altittude),
            (44.548962,	11.416390, altittude),
            (44.548946,	11.416425, altittude),
            (44.549831,	11.417106, altittude)]

dronecore.take_off(vehicle, 2)
dronecore.simple_goto(vehicle, waypoints, 2)
dronecore.status_info(vehicle)

#vehicle.mode = VehicleMode("LAND")
vehicle.close()

