import time, logging, select
from dronecore import dronecore, spacenav
from dronekit import connect

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def main():
    navigator = spacenav.Navigator("3Dconnexion SpaceNavigator")
   #vehicle = dronecore.Vehicle('udp:127.0.0.1:14553')


    #vehicle.check_n_arm()
    #vehicle.take_off(2)

    while True:
        select.select([navigator.dev_obj], [], [])
        navigator.get_values(max_value=8, cut_value=10, min_value=0)

        #vehicle.channels.overrides = {'1': navigator.mapped_pos[4], '2': navigator.mapped_pos[3],'4':navigator.mapped_pos[5]}        

        #if navigator.mapped_neg[2] > 0: vehicle.move_up(1)
        #elif navigator.mapped_neg[2] < 0: vehicle.move_down()
        #elif navigator.mapped_neg[3] > 0: vehicle.move_forward(abs(navigator.mapped_neg[3]))
        #elif navigator.mapped_neg[3] < 0: vehicle.move_backward(abs(navigator.mapped_neg[3]))
        #elif navigator.mapped_neg[4] > 0: vehicle.move_right(abs(navigator.mapped_neg[4]))
        #elif navigator.mapped_neg[4] < 0: vehicle.move_left(abs(navigator.mapped_neg[4]))


        logging.debug(str(navigator.axispos))
        #logging.debug(str(navigator.buttons))
        #logging.debug(str(navigator.mapped_neg))

    #vehicle.close()


if __name__ == "__main__":
    main()

               