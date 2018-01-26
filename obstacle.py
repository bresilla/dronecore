import time, logging, sys, signal
#from dronecore import dronecore
#from dronekit import connect
from PyMata.pymata import PyMata

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def main():
    #vehicle = connect('udp:192.168.1.177:14554', baud=57600, wait_ready=True)
    #vehicle = connect('udp:10.42.0.1:14555', baud=57600, wait_ready=True)
    #vehicle = connect('udp:127.0.0.1:14553', baud=57600, wait_ready=True)

    arduino = PyMata("/dev/ttyUSB0")

    arduino.sonar_config(3, 4)
    arduino.sonar_config(5, 6)
    arduino.sonar_config(7, 8)

    def signal_handler(signal, frame):
        if arduino != None:
            arduino.reset()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        arduino.digital_write(13, 1)
        data = arduino.get_sonar_data()

        sonarS = data[3][1]
        sonarL = data[5][1]
        sonarR = data[7][1]

        print sonarS, sonarR, sonarL

        
        time.sleep(.05)

    #vehicle.mode = VehicleMode("LAND")
    #vehicle.close()
    arduino.close()

if __name__ == "__main__":
    main()
