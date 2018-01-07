import time, logging, select
import evdev
from dronecore import devices, dronecore, spacenav, controller
from dronekit import connect

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def main():
    #joystick = controller.Joystick("Microsoft X-Box One S pad")
    #navigator = spacenav.Navigator("3Dconnexion SpaceNavigator")
    #vehicle = dronecore.Vehicle('udp:127.0.0.1:14553')
    
    time_dest = 5
    count_chk = 0


    while False:
        select.select([navigator.dev_obj], [], [])
        navigator.get_values(cut_value=25)

        #vehicle.channels.overrides = {'1': navigator.mapped_pos[4], '2': navigator.mapped_pos[3],'4':navigator.mapped_pos[5]}        

        if navigator.mapped_neg[2] > 0: vehicle.move_up(1)
        elif navigator.mapped_neg[2] < 0: vehicle.move_down()
        elif navigator.mapped_neg[3] > 0: vehicle.move_forward(abs(navigator.mapped_neg[3]))
        elif navigator.mapped_neg[3] < 0: vehicle.move_backward(abs(navigator.mapped_neg[3]))
        elif navigator.mapped_neg[4] > 0: vehicle.move_right(abs(navigator.mapped_neg[4]))
        elif navigator.mapped_neg[4] < 0: vehicle.move_left(abs(navigator.mapped_neg[4]))




        #logging.debug(str(joystick.axs1_mapped))
        #logging.debug(str(joystick.axs2_mapped))

    
    while False:
        select.select([joystick.dev_obj], [], [])
        joystick.get_values(max_value=10, cut_value=50)



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




        if joystick.axs1_mapped[0] > 0: vehicle.move_up(0.5)
        elif joystick.axs1_mapped[1] > 0: vehicle.move_down(0.5)
        elif joystick.axs2_mapped[0] > 0: vehicle.move_forward((joystick.axs2_mapped[0]/10)+(joystick.trig_mapped[0])+(joystick.trig_mapped[1]/2))
        elif joystick.axs2_mapped[1] > 0: vehicle.move_backward((joystick.axs2_mapped[1]/10)+(joystick.trig_mapped[0])+(joystick.trig_mapped[1]/2))
        elif joystick.axs2_mapped[2] > 0: vehicle.move_left((joystick.axs2_mapped[2]/10)+(joystick.trig_mapped[0])+(joystick.trig_mapped[1]/2))
        elif joystick.axs2_mapped[3] > 0: vehicle.move_right((joystick.axs2_mapped[3]/10)+(joystick.trig_mapped[0])+(joystick.trig_mapped[1]/2))


        #logging.debug(str(joystick.axs1_mapped))
        logging.debug(str(joystick.axs2_mapped))    

    devices.get_devices()



    

def mapit(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

if __name__ == "__main__":
    main()