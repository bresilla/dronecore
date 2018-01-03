import time, logging
from dronecore import dronecore, sensata
from dronekit import connect

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def main():
    vehicle = connect('udp:192.168.1.177:14554', baud=57600, wait_ready=True)
    #vehicle = connect('udp:10.42.0.1:14555', baud=57600, wait_ready=True)
    #vehicle = connect('udp:127.0.0.1:14553', baud=57600, wait_ready=True)

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


if __name__ == "__main__":
    main()
