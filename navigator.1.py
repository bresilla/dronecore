import time, logging, select
import evdev
from dronecore import dronecore, controller
from dronekit import connect

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def joistick_cont():
    joystick = controller.Joystick("Microsoft X-Box One S pad")
    while True:
        select.select([joystick.dev_obj], [], [])
        joystick.get_values()

        logging.debug(str(joystick.mapped_pos))
        logging.debug(str(joystick.mapped_neg))


def navigator_cont():
    navigator = controller.Navigator("3Dconnexion SpaceNavigator")
    while True:
        select.select([navigator.dev_obj], [], [])
        navigator.get_values()
        
        logging.debug(str(navigator.mapped_pos))
        logging.debug(str(navigator.mapped_neg))


def transmitter_cont():
    transmitter = controller.Transmitter("Flysky FS-i6S emulator")
    while True:
        select.select([transmitter.dev_obj], [], [])
        transmitter.get_values()
        
        logging.debug(str(transmitter.mapped_pos))
        logging.debug(str(transmitter.mapped_neg))

def vehicle_start():
    vehicle = dronecore.Vehicle('udp:127.0.0.1:14553')
    vehicle.check_n_arm()
    vehicle.take_off(20)

def list_devices():
    controller.get_devices()

def main():
    
    time_dest = 5
    count_chk = 0

        #vehicle.channels.overrides = {'1': navigator.mapped_pos[4], '2': navigator.mapped_pos[3],'4':navigator.mapped_pos[5]}        

    if joystick.menu[0] and joystick.menu[1]:
        count_chk +=1
        time.sleep(1)
        if count_chk > time_dest:
            joystick.menu[0], joystick.menu[1] = 0, 0
            count_chk = 0
            vehicle.change_mode("LAND")
    elif joystick.stik[0] and joystick.stik[1]:
        count_chk +=1
        time.sleep(1)
        if count_chk > time_dest:
            joystick.stik[0], joystick.stik[1] = 0, 0
            count_chk = 0
            vehicle.change_mode("RTL")
    elif joystick.butt[0] and joystick.butt[1]:
        count_chk +=1
        time.sleep(1)
        if count_chk > time_dest:
            joystick.butt[0], joystick.butt[1] = 0, 0
            count_chk = 0
            vehicle.check_n_arm()
            vehicle.take_off(2)
    else: count_chk = 0

if __name__ == "__main__":
    joistick_cont()