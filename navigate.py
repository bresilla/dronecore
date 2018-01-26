import time, logging
from dronecore import dronecore
from dronekit import connect

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def main():
    vehicle = connect('udp:192.168.1.177:14553', baud=57600, wait_ready=True)
    #vehicle = connect('udp:10.42.0.1:14555', baud=57600, wait_ready=True)
    #vehicle = connect('udp:127.0.0.1:14553', baud=57600, wait_ready=True)

    dronecore.check_n_arm(vehicle)
    dronecore.status_info(vehicle) 

    ######################
    dronecore.take_off(vehicle, 2)

    dronecore.move_forward(vehicle, 10)


    vehicle.close()

if __name__ == "__main__":
    main()
