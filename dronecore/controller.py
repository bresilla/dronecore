import evdev
import logging
from select import select

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def main():
    controller = Joystick("Microsoft X-Box One S pad")
    while True:
        select([controller.dev_obj], [], [])
        controller.get_values()

class Joystick():
    def mapit(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

    def percentage(self, percent, whole):
        if percent == 0: return 0
        else: return int((percent * whole) / 100.0)

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
        self.axs1 = [0, 0, 0, 0]
        self.axs2 = [0, 0, 0, 0]
        self.trig = [0, 0]

        self.arro = [0, 0, 0, 0]
        self.abxy = [0, 0, 0, 0]
        self.stik = [0, 0]
        self.butt = [0, 0]
        self.menu = [0, 0]
        
        
        self.axs1_cutted = None
        self.axs2_cutted = None
        self.trig_cutted = None

        self.trig_mapped = None
        self.trig_mapped = None
        self.trig_mapped = None


    def get_values(self, max_value=100, cut_value=10):
        if max_value < 0: max_value = abs(max_value)
        cut_value = self.percentage(cut_value, 1023)
        event_gen = self.dev_obj.read()
        if event_gen is not None:
            for event in event_gen:
                if event.type == 3:
                    if event.code == 16:
                        if event.value == -1: self.arro[2] = abs(int(event.value))
                        elif event.value == 1: self.arro[3] = abs(int(event.value))
                        else: self.arro[3], self.arro[2] = 0, 0
                    elif event.code == 17:
                        if event.value == -1: self.arro[0] = abs(int(event.value))
                        elif event.value == 1: self.arro[1] = abs(int(event.value))
                        else: self.arro[0], self.arro[1] = 0, 0
                    
                    elif event.code == 2:self.trig[0] = int(event.value)
                    elif event.code == 5:self.trig[1] = int(event.value)

                    elif event.code == 1:
                        if event.value < 0:self.axs1[0] = int(self.mapit(abs(event.value), 0, 32768, 0, 1023))
                        elif event.value > 0:self.axs1[1] = int(self.mapit(abs(event.value), 0, 32767, 0, 1023))
                    elif event.code == 0:
                        if event.value < 0:self.axs1[2] = int(self.mapit(abs(event.value), 0, 32768, 0, 1023))
                        elif event.value > 0:self.axs1[3] = int(self.mapit(abs(event.value), 0, 32767, 0, 1023))
                    
                    elif event.code == 4:
                        if event.value < 0:self.axs2[0] = int(self.mapit(abs(event.value), 0, 32768, 0, 1023))
                        elif event.value > 0:self.axs2[1] = int(self.mapit(abs(event.value), 0, 32767, 0, 1023))
                    elif event.code == 3:
                        if event.value < 0:self.axs2[2] = int(self.mapit(abs(event.value), 0, 32768, 0, 1023))
                        elif event.value > 0:self.axs2[3] = int(self.mapit(abs(event.value), 0, 32767, 0, 1023))
                
                self.axs1_cutted = [0 if i < cut_value else self.mapit(i, cut_value, 1023, 0, 1023-cut_value) for i in self.axs1]
                self.axs2_cutted = [0 if i < cut_value else self.mapit(i, cut_value, 1023, 0, 1023-cut_value) for i in self.axs2]
                self.trig_cutted = [0 if i < cut_value else self.mapit(i, cut_value, 1023, 0, 1023-cut_value) for i in self.trig]

                self.axs1_mapped = [self.mapit(i, 0, 1023-cut_value, 0, max_value) for i in self.axs1_cutted]
                self.axs2_mapped = [self.mapit(i, 0, 1023-cut_value, 0, max_value) for i in self.axs2_cutted]
                self.trig_mapped = [self.mapit(i, 0, 1023-cut_value, 0, max_value) for i in self.trig_cutted]


                if event.type == 1:                   
                    if event.code == 304: self.abxy[0] = int(event.value)
                    elif event.code == 305: self.abxy[1] = int(event.value)
                    elif event.code == 307: self.abxy[2] = int(event.value)
                    elif event.code == 308: self.abxy[3] = int(event.value)

                    elif event.code == 310: self.butt[0] = int(event.value)
                    elif event.code == 311: self.butt[1] = int(event.value)

                    elif event.code == 314: self.menu[0] = int(event.value)
                    elif event.code == 315: self.menu[1] = int(event.value)

                    elif event.code == 317: self.stik[0] = int(event.value)
                    elif event.code == 318: self.stik[1] = int(event.value)
                    
        #logging.debug(str(self.axs1_mapped))
        #logging.debug(str(self.axs2_mapped))
        #logging.debug(str(self.trig_cutted))
        #logging.debug(str(self.arro)+str(self.abxy)+str(self.stik)+str(self.butt)+str(self.menu))
        

if __name__ == "__main__":
    main()