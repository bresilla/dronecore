import evdev
import logging
from select import select

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def main():
    controller = Navigator("3Dconnexion SpaceNavigator")
    while True:
        select([controller.dev_obj], [], [])
        controller.get_values()
        print controller.values


class Navigator():
    def mapit(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

    def __init__(self, controller_name):

        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        dev_location = None
        for dev in devices:
            if dev.name == controller_name:
                dev_location = dev.fn
                logging.debug("Device found: " + dev.name + " at: " + dev.fn)
                break
        if dev_location is None:
            raise "Device not found!"

        self.dev_obj = evdev.InputDevice(dev_location)
        self.axispos = [0, 0, 0, 0, 0, 0]
        self.buttons = [0, 0]
        self.mapped_neg = None
        self.mapped_pos = None

    def get_values(self, max_value=100, cut_value=1, min_value=0):
        if max_value < 0: max_value = abs(max_value)
        if cut_value > 20: cut_value=20
        if cut_value < 1: cut_value=1
        if min_value < 0: min_value=0
        if min_value > max_value: min_value=0
        event_gen = self.dev_obj.read()
        if event_gen is not None:
            for event in event_gen:
                if event.type == 2:
                    if event.code == 0:
                        self.axispos[0] = int(event.value)
                    elif event.code == 1:
                        self.axispos[1] = int(self.mapit(event.value, -350, 350, 350, -350))
                    elif event.code == 2:
                        self.axispos[2] = int(self.mapit(event.value, -350, 350, 350, -350))
                    elif event.code == 3:
                        self.axispos[3] = int(self.mapit(event.value, -350, 350, 350, -350))
                    elif event.code == 4:
                        self.axispos[4] = int(self.mapit(event.value, -350, 350, 350, -350))
                    elif event.code == 5:
                        self.axispos[5] = int(event.value)
                self.axispos = [0 if abs(i) < cut_value*10 else i for i in self.axispos]
                self.mapped_neg = [0 if abs(i) < cut_value*10 else self.mapit(i, -cut_value*10, -350, 0, -max_value) if i < 0 else self.mapit(i, cut_value*10, 350, 0, max_value) for i in self.axispos]
                self.mapped_pos = [(max_value+min_value)/2 if abs(i) < cut_value*10 else self.mapit(i, -cut_value*10, -350, (max_value+min_value)/2, min_value) if i < 0 else self.mapit(i, cut_value*10, 350, (max_value+min_value)/2, max_value) for i in self.axispos]

                if event.type == 1:
                    if event.code == 256:
                        self.buttons[0] = int(event.value)
                    elif event.code == 257:
                        self.buttons[1] = int(event.value)
                    
        #logging.debug(str(self.axispos))
        #logging.debug(str(self.buttons))
        

if __name__ == "__main__":
    main()