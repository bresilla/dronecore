import time, logging, evdev
from select import select

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def get_devices():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        logging.debug(str(device))

def get_values_name(name):
    port = None
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        #print device
        if device.name == name:
            port = device.fn
            print port
    if port:
        device = evdev.InputDevice(port)
        for event in device.read_loop():
            typ = event.type
            cod = event.code
            val = int(event.value)
            logging.debug(str(typ) +" "+ str(cod) +" "+ str(val))

def get_values_port(port):
    device = evdev.InputDevice(port)
    for event in device.read_loop():
        typ = event.type
        cod = event.code
        val = int(event.value)
        logging.debug(str(typ) +" "+ str(cod) +" "+ str(val))

def mapit(i, in_min, in_max, out_min, out_max):
    return (i - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def percentage(percent, whole):
    if percent == 0: return 0
    else: return int((abs(percent) * whole) / 100.0)

def curvit(i, pwr_value, max_value):
    if pwr_value < 2: 
        pwr_value = 2
    in_pwr_value = abs(i)**pwr_value
    if i < 0: return mapit(in_pwr_value, 1, max_value**pwr_value, 0, -max_value)
    elif i > 0: return mapit(in_pwr_value, 1, max_value**pwr_value, 1, max_value)
    else: return 0

def mapneg(i, max_value, cut_value, precision):
    if abs(i) < cut_value: return 0 
    elif i < 0: return mapit(i, -cut_value, -precision, 0, -max_value)
    elif i > 0: return mapit(i, cut_value, precision, 0, max_value)

def cuttit(i, cut_value, precision):
    if abs(i) < cut_value: return 0 
    elif i < 0:  return mapit(i, -cut_value, -precision, 0, -precision+cut_value) 
    elif i > 0:  return mapit(i, cut_value, precision, 0, precision-cut_value)
    
    
class Transmitter():
    def __init__(self, controller_name="Flysky FS-i6S emulator"):

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
        self.axis = [0, 0, 0, 0]

        self.button = [0, 0]
        self.switch = [0, 0]
        self.flymod = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.tempswitch = [0, 0]

        self.cutted = None
        self.mapped = None
        self.curved = None
        self.mappos = None

    def get_values(self, max_value=100, cut_value=10, pwr_value=2, min_value=0, self_centered=False):
        precision=100
        if max_value < 0: max_value = abs(max_value)
        if min_value < 0 or min_value > max_value: min_value = 0
        cut_value = percentage(cut_value, precision)
        event_gen = self.dev_obj.read()
        if event_gen is not None:
            for event in event_gen:
                if event.type == 3:
                    if event.code == 0:
                        self.axis[3] = int(mapit(event.value, 21, 232, -precision, precision))
                    elif event.code == 1:
                        self.axis[2] = int(mapit(event.value, 21, 232, -precision, precision))
                    elif event.code == 2:
                        if not self_centered:
                            self.axis[0] = int(mapit(event.value, 21, 232, 0, precision))
                    elif event.code == 3:
                        self.axis[1] = int(mapit(event.value, 21, 232, -precision, precision))

                self.cutted = [cuttit(i, cut_value, precision) for i in self.axis]
                self.mapped = [mapneg(i, max_value, cut_value, precision) for i in self.axis]
                self.curved = [curvit(i, pwr_value, max_value) for i in self.mapped]
                self.mappos = [mapit(i, -max_value, max_value, min_value, max_value) for i in self.mapped]
                
                if not self_centered:
                    self.mappos[0] = mapit(self.mapped[0], 0, max_value, min_value, max_value)

                if event.type == 1:
                    if event.code == 294: self.button[0] = int(event.value)
                    elif event.code == 295: self.button[1] = int(event.value)
                    elif event.code == 293: self.switch[1] = int(event.value)
                    elif event.code == 288: self.switch[0] = abs(int(event.value)-1)


                    if event.code == 290 and event.value == 1: self.tempswitch[0] = 0
                    elif event.code == 290 and event.value == 0: self.tempswitch[0] = 1
                    elif event.code == 289 and event.value == 0: self.tempswitch[0] = 1
                    elif event.code == 289 and event.value == 1: self.tempswitch[0] = 2

                    if event.code == 292 and event.value == 1: self.tempswitch[1] = 0
                    elif event.code == 292 and event.value == 0: self.tempswitch[1] = 1
                    elif event.code == 291 and event.value == 0: self.tempswitch[1] = 1
                    elif event.code == 291 and event.value == 1: self.tempswitch[1] = 2
                
                if self.tempswitch[0] == 0 and self.tempswitch[1] == 0: self.flymod = [1, 0, 0, 0, 0, 0, 0, 0, 0]
                elif self.tempswitch[0] == 1 and self.tempswitch[1] == 0: self.flymod = [0, 1, 0, 0, 0, 0, 0, 0, 0]
                elif self.tempswitch[0] == 2 and self.tempswitch[1] == 0: self.flymod = [0, 0, 1, 0, 0, 0, 0, 0, 0]
                elif self.tempswitch[0] == 2 and self.tempswitch[1] == 1: self.flymod = [0, 0, 0, 1, 0, 0, 0, 0, 0]
                elif self.tempswitch[0] == 1 and self.tempswitch[1] == 1: self.flymod = [0, 0, 0, 0, 1, 0, 0, 0, 0]
                elif self.tempswitch[0] == 0 and self.tempswitch[1] == 1: self.flymod = [0, 0, 0, 0, 0, 1, 0, 0, 0]
                elif self.tempswitch[0] == 0 and self.tempswitch[1] == 2: self.flymod = [0, 0, 0, 0, 0, 0, 1, 0, 0]
                elif self.tempswitch[0] == 1 and self.tempswitch[1] == 2: self.flymod = [0, 0, 0, 0, 0, 0, 0, 1, 0]
                elif self.tempswitch[0] == 2 and self.tempswitch[1] == 2: self.flymod = [0, 0, 0, 0, 0, 0, 0, 0, 1]

                #logging.debug(str(self.axis))
                #logging.debug(str(self.cutted))
                logging.debug(str(self.mapped))
                logging.debug(str(self.curved))
                logging.debug(str(self.mappos))


class Joystick():
    def __init__(self, controller_name="Microsoft X-Box One S pad"): 

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
        self.axis = [0, 0, 0, 0]
        self.trig = [0, 0]

        self.arro = [0, 0, 0, 0]
        self.abxy = [0, 0, 0, 0]
        self.stik = [0, 0]
        self.butt = [0, 0]
        self.menu = [0, 0]
        
        self.trig_cutted = None
        self.trig_mapped = None

        self.cutted = None
        self.mapped = None
        self.curved = None
        self.mappos = None

    def get_values(self, max_value=100, cut_value=10, pwr_value=2, min_value=0):
        precision=1023
        if max_value < 0: max_value = abs(max_value)
        if min_value < 0 or min_value > max_value: min_value = 0
        cut_value = percentage(cut_value, precision)
        event_gen = self.dev_obj.read()
        if event_gen is not None:
            for event in event_gen:
                if event.type == 3:
                    if event.code == 16:
                        if event.value == -1: self.arro[2] = 1
                        elif event.value == 1: self.arro[3] = 1
                        else: self.arro[3], self.arro[2] = 0, 0
                    elif event.code == 17:
                        if event.value == -1: self.arro[0] = 1
                        elif event.value == 1: self.arro[1] = 1
                        else: self.arro[0], self.arro[1] = 0, 0
                    
                    elif event.code == 2:self.trig[0] = int(event.value)
                    elif event.code == 5:self.trig[1] = int(event.value)

                    elif event.code == 1: self.axis[0] = int(mapit(event.value, -32768, 32767, -precision, precision))
                    elif event.code == 0: self.axis[1] = int(mapit(event.value, -32768, 32767, -precision, precision))
                    elif event.code == 4: self.axis[2] = int(mapit(event.value, -32768, 32767, -precision, precision))
                    elif event.code == 3: self.axis[3] = int(mapit(event.value, -32768, 32767, -precision, precision))

                self.cutted = [cuttit(i, cut_value, precision) for i in self.axis]
                self.mapped = [mapneg(i, max_value, cut_value, precision) for i in self.axis]
                self.mappos = [mapit(i, -max_value, max_value, min_value, max_value) for i in self.mapped]
                self.curved = [curvit(i, pwr_value, max_value) for i in self.mapped]

                self.trig_cutted = [0 if i < cut_value else mapit(i, cut_value, precision, 0, precision-cut_value) for i in self.trig]
                self.trig_mapped = [mapit(i, 0, precision-cut_value, 0, max_value) for i in self.trig_cutted]

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
                
                #logging.debug(str(self.axis))
                #logging.debug(str(self.cutted))
                logging.debug(str(self.mapped))
                logging.debug(str(self.curved))
                #logging.debug(str(self.mappos))
                
                    
class Navigator():
    def __init__(self, controller_name="3Dconnexion SpaceNavigator"):

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
        self.axis = [0, 0, 0, 0, 0, 0]
        self.buttons = [0, 0]

        self.cutted = None
        self.mapped = None
        self.curved = None
        self.mappos = None

    def get_values(self, max_value=100, cut_value=10, pwr_value=2, min_value=0):
        precision=350
        if max_value < 0: max_value = abs(max_value)
        if min_value < 0 or min_value > max_value: min_value = 0
        cut_value = percentage(cut_value, precision)
        event_gen = self.dev_obj.read()
        if event_gen is not None:
            for event in event_gen:
                if event.type == 2:
                    if event.code == 0:
                        self.axis[0] = int(event.value)
                    elif event.code == 1:
                        self.axis[1] = int(mapit(event.value, -precision, precision, precision, -precision))
                    elif event.code == 2:
                        self.axis[2] = int(mapit(event.value, -precision, precision, precision, -precision))
                    elif event.code == 3:
                        self.axis[3] = int(event.value)              
                        #self.axis[3] = int(mapit(event.value, -350, 350, 350, -350))
                    elif event.code == 4:
                        self.axis[4] = int(mapit(event.value, -precision, precision, precision, -precision))
                    elif event.code == 5:
                        self.axis[5] = int(event.value)
                
                self.cutted = [cuttit(i, cut_value, precision) for i in self.axis]
                self.mapped = [mapneg(i, max_value, cut_value, precision) for i in self.axis]
                self.mappos = [mapit(i, -max_value, max_value, min_value, max_value) for i in self.mapped]
                self.curved = [curvit(i, pwr_value, max_value) for i in self.mapped]

                if event.type == 1:
                    if event.code == 256: self.buttons[0] = int(event.value)
                    elif event.code == 257: self.buttons[1] = int(event.value)

                
                #logging.debug(str(self.axis))
                #logging.debug(str(self.cutted))
                logging.debug(str(self.mapped))
                logging.debug(str(self.curved))
                #logging.debug(str(self.mappos))
                