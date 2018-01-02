import evdev
import logging
from select import select

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def main():
    controller = Navigator("3Dconnexion SpaceNavigator")
    while True:
        select([controller.dev_obj], [], [])
        controller.get_axis_pos()
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
        self.values = None
        self.mapped = None
        self.cutted = None
        self.mapped_neg = None
        self.mapped_pos = None

    def events_get(self):
        for event in self.dev_obj.read_loop():
            if event.type != 0:
                print(event)

    def get_axis_pos(self, max_value=100, cut_value=1, min_value=0):
        if cut_value > 20: cut_value=20
        event_gen = self.dev_obj.read()
        if event_gen is not None:
            for event in event_gen:
                if event.type == 2:
                    if event.code == 0:
                        self.axispos[0] = event.value
                    elif event.code == 1:
                        self.axispos[1] = event.value
                    elif event.code == 2:
                        self.axispos[2] = event.value
                    elif event.code == 3:
                        self.axispos[3] = event.value
                    elif event.code == 4:
                        self.axispos[4] = event.value
                    elif event.code == 5:
                        self.axispos[5] = event.value
                self.values = map(int, self.axispos)
                self.mapped_ = [self.mapit(-i, 0, 350, 0, max_value) for i in self.values]
                self.cutted = [0 if abs(i) < cut_value*10 else i for i in self.values]
                self.mapped_neg = [0 if abs(i) < cut_value*10 else self.mapit(i, -cut_value*10, -350, 0, -max_value) if i < 0 else self.mapit(i, cut_value*10, 350, 0, max_value) for i in self.cutted]
                self.mapped_pos = [0 if abs(i) < cut_value*10 else self.mapit(i, -cut_value*10, -350, min_value, (max_value+min_value)/2) if i < 0 else self.mapit(i, cut_value*10, 350, (max_value+min_value)/2, max_value) for i in self.cutted]
                    
        #logging.debug(str(self.axispos))

if __name__ == "__main__":
    main()