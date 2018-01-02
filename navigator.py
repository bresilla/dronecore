import time
from dronecore import dronecore, spacenav
from dronekit import connect
from select import select

#vehicle = connect('udp:192.168.1.177:14555', baud=57600, wait_ready=True)
#vehicle = connect('udp:10.42.0.1:14555', baud=57600, wait_ready=True)

while True:

    navigator = spacenav.Navigator("3Dconnexion SpaceNavigator")
    while True:
        select([navigator.dev_obj], [], [])
        navigator.get_axis_pos(10, 10)
        print navigator.mapped_neg
#vehicle.mode = VehicleMode("LAND")
#vehicle.close()


               