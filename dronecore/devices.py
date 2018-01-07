import evdev
import logging
from select import select

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def get_devices():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        logging.debug(str(device))


def get_values(device):
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        #print device
        if device.name == device:
            port = device.fn
    if port:
        device = evdev.InputDevice(port)
        for event in device.read_loop():
            typ = event.type
            cod = event.code
            val = int(event.value)
            logging.debug(str(typ) +" "+ str(cod) +" "+ str(val))

if __name__ == "__main__":
    pass