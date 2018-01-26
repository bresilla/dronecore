import time, logging, select
from dronecore import dronecore, controller

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def joistick_cont():
    joystick = controller.Joystick("Microsoft X-Box One S pad")
    while True:
        select.select([joystick.dev_obj], [], [])
        joystick.get_values(100, 25, 3)


def navigator_cont():
    navigator = controller.Navigator("3Dconnexion SpaceNavigator")
    while True:
        select.select([navigator.dev_obj], [], [])
        navigator.get_values(100, 25, 3)
        


def transmitter_cont():
    transmitter = controller.Transmitter("Flysky FS-i6S emulator")
    while True:
        select.select([transmitter.dev_obj], [], [])
        transmitter.get_values(2000, 10, 3, 1000)
        

def list_devices():
    controller.get_devices()

if __name__ == "__main__":
    list_devices();
    
    #joistick_cont();
    navigator_cont();
    #transmitter_cont();
